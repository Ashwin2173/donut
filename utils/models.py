import struct

class Constant:
    def __init__(self, value: str) -> None:
        self.value = value
        self.index = None

    def __bytes__(self) -> None:
        raise NotImplementedError("__bytes__ for a constants in not implemented")

class Constant_Utf8(Constant):
    def __init__(self, value):
        super().__init__(value)

    def __bytes__(self) -> bytearray:
        return struct.pack(">BH", 1, len(self.value)) + bytes(self.value, encoding="utf-8")
    
class Constant_String(Constant):
    def __init__(self, value: int):
        super().__init__(value)
    
    def __bytes__(self):
        return struct.pack(">BH", 8, self.value)
    
class Constant_Class(Constant):
    def __init__(self, value: int):
        super().__init__(value)
    
    def __bytes__(self) -> bytearray:
        return struct.pack(">BH", 7, self.value)
    
class Constant_Methodref(Constant):
    def __init__(self, class_index: int, name_and_type_index: int):
        super().__init__(name_and_type_index)
        self.class_index = class_index

    def __bytes__(self) -> bytes:
        return struct.pack(">BHH", 10, self.class_index, self.value)
    
class Constant_NameAndType(Constant):
    def __init__(self, name_index, descriptor_index):
        super().__init__(name_index)
        self.descriptor_index = descriptor_index
    
    def __bytes__(self):
        return struct.pack(">BHH", 12, self.value, self.descriptor_index)
