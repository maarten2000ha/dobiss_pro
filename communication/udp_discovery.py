import socket


def udp_discovery():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(10)

    server_address = ('255.255.255.255', 30718)
    message = bytearray([0, 0, 0, 248])

    try:
        while True:
            sock.sendto(message, server_address)
            _, server = sock.recvfrom(4096)
            if server[0]:
                return str(server[0])

    finally:
        sock.close()
