import ipaddress
import re
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil


class NetworkScanner:

    DISCOVERY_PORTS = (
        445,
        3389,
        22,
        80,
        443,
        135,
        139,
        5985,
    )

    def __init__(self, threads=500, timeout=0.15):
        self.threads = threads
        self.timeout = timeout

    def _interfaces(self):
        interfaces = []

        for name, addresses in psutil.net_if_addrs().items():
            ipv4 = None
            netmask = None

            for address in addresses:
                if address.family == socket.AF_INET:
                    ipv4 = address.address
                    netmask = address.netmask
                    break

            if not ipv4 or not netmask:
                continue

            try:
                network = ipaddress.ip_network(
                    f"{ipv4}/{netmask}",
                    strict=False
                )
            except ValueError:
                continue

            if network.is_loopback or network.is_link_local:
                continue

            interfaces.append((ipv4, network))

        return interfaces

    def _networks(self):
        networks = []

        for ip, network in self._interfaces():
            if network.prefixlen < 24:
                network = ipaddress.ip_network(
                    f"{ip}/24",
                    strict=False
                )

            if network not in networks:
                networks.append(network)

        return networks

    def _reachable(self, ip):
        for port in self.DISCOVERY_PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)

            try:
                result = sock.connect_ex((str(ip), port))

                if result in (0, 10061, 111):
                    return str(ip)

            except OSError:
                pass

            finally:
                sock.close()

        return None

    def _scan(self, network):
        hosts = network.hosts()
        discovered = []

        with ThreadPoolExecutor(
            max_workers=self.threads
        ) as executor:
            futures = [
                executor.submit(self._reachable, ip)
                for ip in hosts
            ]

            for future in as_completed(futures):
                try:
                    ip = future.result()
                except Exception:
                    continue

                if ip:
                    discovered.append(ip)

        return discovered

    def scan(self):
        discovered = []

        for network in self._networks():
            discovered.extend(self._scan(network))

        return sorted(
            set(discovered),
            key=ipaddress.ip_address
        )