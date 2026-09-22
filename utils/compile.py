import struct
from utils.models import *
from utils.exceptions import DonutError
from utils.tokenizer import TokenType, tokenize

class Compiler:
    def __init__(self, program: str):
        self.program = program
        self.tokens = iter(tokenize(self.program))
        self.constant_table = dict()

    def handle_constant(self, constant) -> int:
        if constant.value in self.constant_table: 
            return self.constant_table[constant.value].index
        constant.index = len(self.constant_table) + 1
        self.constant_table[constant.value] = constant
        return constant.index
    
    def handle_function_access_flag(self, name) -> int:
        result = 0
        if name.startswith("__"):   # private
            result |= 0x0002
        elif name.startswith("_"):  # protected
            result |= 0x0004
        else:                       # public
            result |= 0x0001
        result |= 0x0008            # static
        return result
    
    def compile_function_body(self) -> bytearray:
        if next(self.tokens).type != TokenType.K_RETURN:
            raise DonutError("no other op code is accept for now; give just return")
        return struct.pack(">B", 0xB1)
    
    def compile_function(self) -> bytearray:
        bc = bytearray()
        function_name = next(self.tokens)
        bc += struct.pack(">H", self.handle_function_access_flag(function_name.raw))
        bc += struct.pack(">H", self.handle_constant(Constant_Utf8(function_name.raw)))
        expect(next(self.tokens), TokenType.OPEN_PARAM)
        bc += struct.pack(">H", self.handle_constant(Constant_Utf8("([Ljava/lang/String;)V")))
        expect(next(self.tokens), TokenType.CLOSE_PARAM)
        expect(next(self.tokens), TokenType.OPEN_BRACE)
        bc += struct.pack(">H", 1)  # attr count
        bc += struct.pack(">H", self.handle_constant(Constant_Utf8("Code")))
        code_length = len(bc)
        bc += struct.pack(">L", 0)  # code attr length
        bc += struct.pack(">H", 1) # max stack
        bc += struct.pack(">H", 1) # max local
        body = self.compile_function_body()
        bc += struct.pack(">L", len(body))
        bc += body
        bc += struct.pack(">H", 0) # exception table
        bc += struct.pack(">H", 0) # attribute table
        length = len(bc)
        bc[code_length:code_length+4] = struct.pack(">L", length - (code_length+4))
        expect(next(self.tokens), TokenType.CLOSE_BRACE)
        return bc

    def compile(self) -> bytearray:
        bc = bytearray([0xCA, 0xFE, 0xBA, 0xBE])
        bc += struct.pack(">H", 0)   # major
        bc += struct.pack(">H", 62)  # minor
        func_bc = bytearray()
        func_count = 0
        for token in self.tokens:
            if token.type == TokenType.K_FUNCTION:
                func_bc += self.compile_function()
                func_count += 1
            elif token.type == TokenType.K_EOF:
                break
            else:
                raise DonutError(token, f"Invalid syntax (debug: {token.raw})")
        bc += self.pack_compiled(func_count, func_bc)
        return bc
        
    def pack_compiled(self, func_count, func_bc) -> bytearray:
        bc = bytearray()
        this_class_name = self.handle_constant(Constant_Utf8("Main"))
        this_class_index = self.handle_constant(Constant_Class(this_class_name))
        super_class_name = self.handle_constant(Constant_Utf8("java/lang/Object"))
        super_class_index = self.handle_constant(Constant_Class(super_class_name))
        source_file = self.handle_constant(Constant_Utf8("SourceFile"))
        source_file_index = self.handle_constant(Constant_Utf8("Main.dt"))
        const_in_order = [None] * len(self.constant_table)
        for const in self.constant_table.values():
            const_in_order[const.index - 1] = const
        bc += struct.pack(">H", len(const_in_order) + 1)
        for const in const_in_order:
            bc += bytes(const)
        bc += struct.pack(">H", 1)  # public access-flag
        bc += struct.pack(">H", this_class_index)
        bc += struct.pack(">H", super_class_index)
        bc += struct.pack(">H", 0)  # interface count
        bc += struct.pack(">H", 0)  # fields count
        bc += struct.pack(">H", func_count)
        bc += func_bc
        bc += struct.pack(">H", 1)  # class attrs
        bc += struct.pack(">H", source_file)
        bc += struct.pack(">L", 2)
        bc += struct.pack(">H", source_file_index)
        return bc
        
def expect(token, type):
    if token.type != type:
        raise DonutError(token, f"expected {type} got {token.raw}")
    return token