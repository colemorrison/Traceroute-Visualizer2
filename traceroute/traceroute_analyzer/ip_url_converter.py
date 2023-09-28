# need to add documentation and could handle error more apprioptly. Addtional, the Abstract base class might be unessury since you dont plan on adding more thin one subclass
import socket
from abc import ABC, abstractmethod


class AbstractIpUrlConverter(ABC):
    @abstractmethod
    def ip_or_url_to_ip(ip_or_url: str) -> str:
        pass

    @abstractmethod
    def ip_or_url_to_url(ip_or_url: str) -> str:
        pass


class IpUrlConverter(AbstractIpUrlConverter):
    @staticmethod
    def ip_or_url_to_ip(ip_or_url: str) -> str:
        try:
            return socket.gethostbyname(ip_or_url)
        except (socket.gaierror, socket.herror):
            raise ValueError(f"Invalid IP or URL: {ip_or_url}")

    @staticmethod
    def ip_or_url_to_url(ip_or_url: str) -> str:
        try:
            return socket.gethostbyaddr(ip_or_url)[0]
        except (socket.gaierror, socket.herror):
            raise ValueError(f"Invalid IP or URL: {ip_or_url}")
