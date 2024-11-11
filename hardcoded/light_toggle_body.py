from util import convert_brightness_to_hex


class LightToggleBody:
    def __init__(self, module_id, light_id):
        self.module_id = module_id
        self.light_id = light_id
    def get_bytearrays(self, brightness: int):
        brightness_hex  = convert_brightness_to_hex(brightness)
        header = bytearray.fromhex(f"AF 02 ff {self.module_id} 00 00 08 01 08 FF FF FF FF FF FF AF")
        body = bytearray.fromhex(f"{self.module_id} {self.light_id} 02 ff ff {brightness_hex} ff ff")
        return [header, body]

