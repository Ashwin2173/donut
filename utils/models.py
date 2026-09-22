import struct

class Constant:
    def __init__(self, value: str) -> None:
        self.value = value
        self.index = None

class Constant_Utf8(Constant):
    def __init__(self, value):
        super().__init__(value)

    def __bytes__(self) -> bytearray:
        return struct.pack(">BH", 1, len(self.value)) + bytes(self.value, encoding="utf-8")
    
class Constant_Class(Constant):
    def __init__(self, value):
        super().__init__(value)
    
    def __bytes__(self) -> bytearray:
        return struct.pack(">BH", 7, self.value)