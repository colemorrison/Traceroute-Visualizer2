# need to add documentation. Addtional, maybe include and abstract base class. also, check for correct ranges
from typing import List, Union, Optional  # Used for Type hints


class RouterData:
    def __init__(self, ip: Optional[str], ip_type: Optional[str], response_times: Optional[List[Optional[Union[int, float]]]], router_number: Optional[int], coordinates: Optional[List[Optional[float]]]):

        # Implementing Defensive Programming and the Fail Fast philosophy by checking for correct types.
        # Considering the project's scale, extensive type checking might be excessive.

        if ip is not None and not isinstance(ip, str):
            raise TypeError("ip must be a string or None")

        if ip_type is not None and not isinstance(ip_type, str):
            raise TypeError("ip_type must be a string or None")

        if response_times is not None and not all(isinstance(rt, (int, float, type(None))) for rt in response_times):
            raise TypeError(
                "response_times must be a list of integers, floats, or Nones")

        if router_number is not None and not isinstance(router_number, int):
            raise TypeError("router_number must be an integer or None")

        if coordinates is not None and not all(isinstance(coord, (int, float, type(None))) for coord in coordinates):
            raise TypeError(
                "coordinates must be a list of floats or Nones")

        self.ip = ip
        self.ip_type = ip_type
        self.response_times = response_times
        self.router_number = router_number
        self.coordinates = coordinates
        self.average_response_time = self._calculate_average_response_time()

    def _calculate_average_response_time(self) -> Union[float, None]:
        if self.response_times is not None and len(self.response_times) > 0:
            return round(sum(self.response_times) / len(self.response_times), 2)
        return None

    def __str__(self) -> str:
        return f"Router Number: {self.router_number}, IP: {self.ip}, IP Type: {self.ip_type}, Response Times: {self.response_times} ms, Avg Response Time: {self.average_response_time} ms, Coordinates: {self.coordinates}"
