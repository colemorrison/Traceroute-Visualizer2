
import time
from typing import Generator, List, Union, Optional  # Used for Type hints
import ipaddress  # uses to determine if it a public or private ip

from traceroute.traceroute_analyzer.router_data import RouterData
from traceroute.traceroute_analyzer.ip_packet_sender import AbstractIpPacket
from traceroute.traceroute_analyzer.coordinates_converter import AbstractCoordinatesConverter


class TracerouteAnalyzer:
    def __init__(self, packet_generator: AbstractIpPacket, coordinates_converter: AbstractCoordinatesConverter, ip: str = "8.8.8.8", ttl: int = 30, ping_attempts: int = 3, coordinate_offset_multiplier: float = 0.01):
        # Implementing Defensive Programming and the Fail Fast philosophy by checking for correct types.
        if not (isinstance(packet_generator, AbstractIpPacket) and isinstance(coordinates_converter, AbstractCoordinatesConverter) and isinstance(ip, str) and isinstance(ttl, int) and isinstance(ping_attempts, int) and isinstance(coordinate_offset_multiplier, float)):
            raise TypeError("Invalid input types.")

        if not (0 < ttl <= 255 and 0 < ping_attempts <= 10 and 0 <= coordinate_offset_multiplier <= 1):
            raise ValueError("Parameter values are out of range.")

        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError("Invalid destination IP address.")

        self.packet_generator = packet_generator
        self.coordinates_converter = coordinates_converter
        self.destination_ip = ip
        self.ttl = ttl
        self.ping_attempts = ping_attempts
        self.coordinate_offset_multiplier = coordinate_offset_multiplier

        self.router_info_list = []

    def _delay_info_for_single_router(self, ttl: int) -> RouterData:
        ip = None
        ip_type = 'private'
        response_times = []
        router_number = ttl
        coordinates = [None, None]

        self.packet_generator.construct_packet(self.destination_ip, ttl)

        for j in range(self.ping_attempts):
            start = time.time()
            router_response = self.packet_generator.send_packet()
            stop = round((time.time() - start) * 1000)
            response_times.append(stop)

        if router_response is not None:
            ip = router_response.src
            ip_type = DetermineIpType.determine_public_or_private_ip(ip)

            if ip_type == 'public':
                coordinates = self.coordinates_converter.ip_to_coordinates(ip)
               # --> maybe there is a better place for adding corrinate offset mutliper maybe in a differne class
                coordinates = [coordinates[0] + (self.coordinate_offset_multiplier * ttl),
                               coordinates[1] + (self.coordinate_offset_multiplier * ttl)]
        else:
            return None

        try:
            router_info = RouterData(
                ip, ip_type, response_times, router_number, coordinates)

            return router_info
        except Exception as e:
            print("Error: ",  e)
            return None

    def tracert_generator(self) -> Generator[Optional[RouterData], None, None]:
        for current_ttl in range(1, self.ttl + 1):
            router_info = self._delay_info_for_single_router(current_ttl)
            if router_info is None:
                continue
            yield router_info
            print("\n\n\n\n\n", router_info, "\n\n\n")
            if router_info.ip == self.destination_ip:
                print("Route finished")
                break


class DetermineIpType:
    @staticmethod
    def determine_public_or_private_ip(ip_address: str) -> str:
        try:
            ip_obj = ipaddress.ip_address(ip_address)
            if ip_obj.is_private:
                return "private"
            else:
                return "public"
        except ValueError:
            return "unknown"
        except Exception as e:
            return f"error: {e}"
