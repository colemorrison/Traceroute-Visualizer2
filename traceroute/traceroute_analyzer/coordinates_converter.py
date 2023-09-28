# need to add documentation and could handle error more apprioptly. Addtional, the Abstract base class might be unessury since you dont plan on adding more thin one subclass
from abc import ABC, abstractmethod
from ip2geotools.databases.noncommercial import DbIpCity
from typing import List, Optional

API_KEY = 'free'


class AbstractCoordinatesConverter(ABC):
    @abstractmethod
    def ip_to_coordinates(self, ip: str) -> Optional[List[float]]:
        pass


class IpToCoordinates(AbstractCoordinatesConverter):
    @staticmethod
    def ip_to_coordinates(ip: str) -> Optional[List[float]]:
        try:
            response = DbIpCity.get(ip, api_key=API_KEY)
            longitude = float(response.longitude)
            latitude = float(response.latitude)
            return [longitude, latitude]
        except DbIpCity.ApiError as api_error:
            print(f"IP to coordinates API error: {api_error}")
            return None
        except Exception as e:
            print(f"Error while converting IP to coordinates: {e}")
            return None
