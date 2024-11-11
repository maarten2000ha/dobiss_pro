def convert_brightness_to_hex(value: int):
    if value >= 100:
        return '0x64'
    return hex(value)
