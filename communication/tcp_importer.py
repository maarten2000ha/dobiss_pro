import logging
import socket


class TcpImporter:
    def __init__(self, ip):
        self.server_address = (ip, 10001)
        self.sock = None
        logging.basicConfig(level=logging.INFO)

    def connect(self):
        """Establish TCP connection to the server."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect(self.server_address)
        except (socket.timeout, socket.error) as e:
            logging.error(f"Failed to connect: {e}")
            self.close_connection()

    def send_command(self, command_data):
        """Send a command to the server and return the response."""
        try:
            self.sock.sendall(command_data)
            response = self.sock.recv(4096)  # Adjust buffer size as needed
            logging.info(response)
            # response = ''.join([self.convert_val(i) for i in response])
            # logging.info(response)
            logging.info(f"Sent command, received response: {response.hex()}")
            return response
        except socket.error as e:
            logging.error(f"Error sending command: {e}")
            return None

    def convert_val(self, value):
        hex_val = '{0:04X}'.format(value)
        inv = hex_val[2:] + hex_val[:2]
        return inv

    def import_installation(self):
        """Import installation configuration."""
        command = bytearray.fromhex("AF 0B 00 00 30 00 10 01 10 FF FF FF FF FF FF AF")
        response = self.send_command(command)

        modules = []


        if response:
            for byte in response:
                print(byte)
            for i in range(16):  # Assuming response byte has relevant module data
                for j in range(8):
                    if response[i] & (1 << j):
                        module_id = i * 8 + j + 1
                        logging.info(f"Module detected: {module_id}")
                        modules.append(module_id)
        return modules

    def import_module_config(self, module_id):
        """Import configuration for a given module."""
        command = bytearray.fromhex(f"AF 10 FF {module_id:02X} 00 00 10 01 10 FF FF FF FF FF FF AF")
        response = self.send_command(command)
        if response:
            logging.info(f"Module {module_id} configuration imported")
            return response
        return None

    def import_groups(self, module_id):
        """Import groups associated with the master module."""
        command = bytearray.fromhex(f"AF 10 20 {module_id:02X} 18 00 20 00 20 FF FF FF FF FF FF AF")
        response = self.send_command(command)
        groups = []  # Parse the response to extract group data
        if response:

            # Here you would parse response bytes to extract groups based on protocol
            groups = self.parse_groups(response)
            logging.info(f"Groups imported for module {module_id}: {groups}")
        return groups

    def import_outputs(self, module):
        """Import output configurations from a module."""
        module_version = 100  # Example version, adjust accordingly
        version_flag = 0x04 if module_version >= 100 else 0x01
        command = bytearray.fromhex(
            f"AF 10 {module['type']:02X} {module['address']:02X} {version_flag:02X} 00 20 {module['output_count']:02X} 20 FF FF FF FF FF FF AF")
        response = self.send_command(command)
        logging.debug(f"outputs: {response}")

        outputs = []  # Parse response to extract output information
        if response:
            # Here you would parse the response bytes to extract outputs based on protocol
            outputs = self.parse_outputs(response, module['output_count'])
            for i in range(module['output_count']):
                logging.info(f"Output {i} for module {module['address']} processed: {outputs[i]}")
        return outputs

    def parse_groups(self, response):
        """Parse the response to extract groups."""
        # Implementation of parsing logic according to your protocol
        # This is a placeholder for actual group parsing
        return [response[i] for i in range(len(response)) if response[i] != 0]

    def parse_outputs(self, response, output_count):
        """Parse the response to extract outputs."""
        # Implementation of parsing logic according to your protocol
        # This is a placeholder for actual output parsing
        return [response[i] for i in range(min(len(response), output_count))]

    def close_connection(self):
        """Close the socket and clean up resources."""
        if self.sock:
            self.sock.close()
            logging.info("Connection closed.")

    def toggle_light(self):
        # command = bytearray.fromhex("AF 01 ff 01 00 00 08 01 00 FF FF FF FF FF FF AF")
        header = bytearray.fromhex("AF 02 ff 02 00 00 08 01 08 FF FF FF FF FF FF AF")
        response = self.send_command(header)
        body = bytearray.fromhex("02 04 00 ff ff 50 ff ff")
        response2 = self.send_command(body)
        # print(f"responsedddd: {response}")
        print(response2)

    def toggle_light_upstairs(self):
        # command = bytearray.fromhex("AF 01 ff 01 00 00 08 01 00 FF FF FF FF FF FF AF")
        header = bytearray.fromhex("AF 02 ff 01 00 00 08 01 08 FF FF FF FF FF FF AF")
        response = self.send_command(header)
        body = bytearray.fromhex("01 00 02 ff ff 50 ff ff")
        response2 = self.send_command(body)
        # print(f"responsedddd: {response}")
        print(response2)

    def execute(self):
        """Main execution method to perform all import steps."""
        try:
            self.connect()
            self.toggle_light_upstairs()

            # modules = self.import_installation()
            #
            # for module_id in modules:
            #     self.import_module_config(module_id)
            #
            # # Assuming master_module is one of the imported modules
            # master_module = {'address': 1, 'type': 0x20, 'output_count': 5}
            # groups = self.import_groups(master_module['address'])
            # outputs = self.import_outputs(master_module)
            #
            # print(f"Imported Groups: {groups}")
            # print(f"Imported Outputs: {outputs}")

        finally:
            self.close_connection()
