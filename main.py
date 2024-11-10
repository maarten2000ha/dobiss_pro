import logging
from communication.tcp_importer import TcpImporter
from communication.udp_discovery import udp_discovery

if __debug__:
    logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    ip = udp_discovery()
    tcp_importer = TcpImporter(ip)
    tcp_importer.execute()
