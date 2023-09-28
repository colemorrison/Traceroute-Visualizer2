from flask import Flask, render_template, request
import jyserver.Flask as jsf
from traceroute.traceroute_analyzer import traceroute_analyzer, ip_packet_sender, coordinates_converter, ip_url_converter
from traceroute.traceroute_geojson import RouterGeoJSONGenerator

flask_app = Flask(__name__)


@flask_app.route('/')  # python decoration this will store the function below it in the flask class so when the page goes to url / it will run the index function that has already been store by the decorector
def index():
    return App.render(render_template('index.html'))


@jsf.use(flask_app)
class App:
    def __init__(self):
        self.ip_or_url = ''
        self.ttl = 30
        self.ping_attempts = 3
        self.ip = ''
        self.url = ''
        self.coordinate_offset_multiplier = 0
        self.router_info_html = ''

    def tracert(self):
        self.clear_map_and_reset_html()
        try:
            self._get_user_input()
        except ValueError as e:
            self._display_error_message(e)
            return

        try:
            self._update_ip_url_stats()
            self._run_tracert_and_display()
        except Exception as e:
            self._display_error_message(e)
            return

    def clear_map_and_reset_html(self):
        self.js.remove_links_and_routers_from_map()
        self.ip_or_url = ''
        self.ttl = 30
        self.ping_attempts = 3
        self.ip = ''
        self.url = ''
        self.coordinate_offset_multiplier = 0
        self.router_info_html = ''
        self._display_router_info_html()
        self.js.document.getElementById(
            "error_message").innerHTML = ''

    def _get_user_input(self):
        ip_or_url_temp = self._get_input_value('destination_url_or_ip')
        ttl_temp = self._get_input_value('ttl')
        ping_attempts_temp = self._get_input_value('ping_attempts')
        coordinate_offset_multiplier_temp = self._get_input_value(
            'coordinate_offset_multiplier')

        if any(value is None for value in [ip_or_url_temp, ttl_temp, ping_attempts_temp, coordinate_offset_multiplier_temp]):
            raise ValueError("One or more values are None.")
        else:
            self.ip_or_url = ip_or_url_temp
            self.ttl = int(ttl_temp)
            self.ping_attempts = int(ping_attempts_temp)
            self.coordinate_offset_multiplier = float(
                coordinate_offset_multiplier_temp)

            self.ip = ip_url_converter.IpUrlConverter.ip_or_url_to_ip(
                self.ip_or_url)
            self.url = ip_url_converter.IpUrlConverter.ip_or_url_to_url(
                self.ip_or_url)

    def _get_input_value(self, element_id):
        return str(self.js.document.getElementById(element_id).value)

    def _construct_traceroute_analyzer(self):
        icmp_packet_generator = ip_packet_sender.IcmpPacket()
        ip_to_coordinates = coordinates_converter.IpToCoordinates()
        traceroute = traceroute_analyzer.TracerouteAnalyzer(icmp_packet_generator, ip_to_coordinates,
                                                            self.ip, self.ttl, self.ping_attempts, self.coordinate_offset_multiplier)
        return traceroute

    def _update_ip_url_stats(self):
        stats_container = self.js.document.getElementById(
            "ip_url_stats_container")
        stats_container.innerHTML = f'<p>IP: {self.ip} URL: {self.url} Ping attempts: {self.ping_attempts} TTL: {self.ttl}</p>'

    def _run_tracert_and_display(self):
        # Runs the Tracert utility on the ip and return
        traceroute = self._construct_traceroute_analyzer()
        router_info_list = traceroute.tracert_generator()
        tracert_to_geojson = RouterGeoJSONGenerator()
        two_routers = []  # used to create a line need two routers so it can draw a line

        for router_info in router_info_list:
            if router_info.ip_type != "private":
                self._display_router_on_map(router_info, tracert_to_geojson)

                # used to check if there is two routers to see if it can create a link line
                two_routers.append(router_info)
                if len(two_routers) == 2:
                    self._display_link_line(two_routers, tracert_to_geojson)
                    two_routers.pop(0)

            self._create_router_info_html(router_info)
            self._display_router_info_html()

    def _display_router_on_map(self, router_info, tracert_to_geojson):
        router_geojson = tracert_to_geojson.create_router_feature(
            coordinates=router_info.coordinates,
            ip_address=router_info.ip,
            ip_type=router_info.ip_type,
            average_response_time=router_info.average_response_time,
            response_times=router_info.response_times,
            router_number=router_info.router_number,
        )
        self.js.load_router_on_map(router_geojson)

    def _display_link_line(self, two_routers, tracert_to_geojson):
        first_router, second_router = two_routers
        link_params = {
            "source_ip": first_router.ip,
            "destination_ip": second_router.ip,
            "start_cord": first_router.coordinates,
            "stop_cord": second_router.coordinates,
            "link_number": first_router.router_number,
        }
        link_geojson = tracert_to_geojson.create_delay_line_feature(
            **link_params)
        self.js.load_link_on_map(link_geojson)

    def _create_router_info_html(self, router_info):
        router_info_html = self._generate_router_info_html(router_info)
        self.router_info_html += router_info_html

    def _display_router_info_html(self):
        self.js.document.getElementById(
            "tracert_output_container").innerHTML = self.router_info_html

    def _generate_router_info_html(self, router_info):
        router_router_number = router_info.router_number
        router_response_times = router_info.response_times
        router_average_response_time = router_info.average_response_time
        router_ip = router_info.ip
        router_ip_type = router_info.ip_type
        return f'''
                <div id="tracert_router_output">
                    <strong>Router {router_router_number}</strong>
                    Response Times: {", ".join(map(str, router_response_times))} ms | <br>
                    Avg Response: {router_average_response_time} ms | IP: {router_ip} | IP Type: {router_ip_type}
                </div>
            '''

    def _display_error_message(self, error):
        self.js.document.getElementById(
            "error_message").innerHTML = f'<p>Error: {error}</p>'


if __name__ == '__main__':
    flask_app.run(debug=True)
