class RouterGeoJSONGenerator:
    def __init__(self):
        self.routers_info = []

    def create_router_feature(self, coordinates, ip_address, ip_type, average_response_time, response_times, router_number):
        return {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': coordinates
                },
                'properties': {
                    'name': router_number,
                    'description': f'IP: {ip_address}\nIP Type: {ip_type}\nAvg Response Time: {average_response_time}\nResponse_times {response_times}'
                }

            }
        }

    def create_delay_line_feature(self, source_ip, destination_ip, start_cord, stop_cord, link_number):
        return {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [
                        start_cord,
                        stop_cord,
                    ]
                },
                'properties': {
                    'name': str(link_number),
                    'description': f'Source IP: {source_ip} Destination IP: {destination_ip}'
                }
            }
        }
