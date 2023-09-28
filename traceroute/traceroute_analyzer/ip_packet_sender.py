# need to add documentation and could handle error more apprioptly
from abc import ABC, abstractmethod
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1

from scapy.packet import Packet
from typing import Optional


class AbstractIpPacket(ABC):
    def __init__(self):
        self.ip_packet = IP()
        self.payload_packet = None
        self.outgoing_packet = None

    @abstractmethod
    def construct_packet(self, destination_ip: str, ttl: int) -> None:
        pass

    @abstractmethod
    def send_packet(self) -> Optional[Packet]:
        pass


class IcmpPacket(AbstractIpPacket):
    def construct_packet(self, destination_ip: str, ttl: int) -> None:
        try:
            self.ip_packet.dst = destination_ip
            self.ip_packet.ttl = ttl

            self.payload_packet = ICMP()
            self.outgoing_packet = self.ip_packet / self.payload_packet

        except Exception as e:
            print(f"An error occurred during packet construction: {e}")
            self.outgoing_packet = None  # Invalidate the packet

    def send_packet(self, timeout: int = 5) -> Optional[Packet]:
        try:
            if self.outgoing_packet:
                icmp_response = sr1(self.outgoing_packet, timeout=timeout)
                return icmp_response
            else:
                print("Packet is not valid for sending.")
                return None
        except Exception as e:
            print(f"An error occurred while sending the packet: {e}")
            return None
