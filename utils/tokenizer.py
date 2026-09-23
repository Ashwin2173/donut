import re
from enum import Enum
from typing import cast

TOKEN_GRAMMAR = r"""
(?P<COMMENT>//[^\n]*)                                     # single-line comment
| (?P<K_FUNCTION>\bfunction\b)                            # function keyword
| (?P<K_RETURN>\breturn\b)                                # return keyword
| (?P<K_PRINT>\bprint\b)                                  # print keyword
| (?P<K_VAR>\bvar\b)                                      # variable declaration
| (?P<OPEN_BRACE>\{)                                      # open brace operator
| (?P<CLOSE_BRACE>\})                                     # close brace operator
| (?P<OPEN_PARAM>\()                                      # open param operator
| (?P<CLOSE_PARAM>\))                                     # close param operator
| (?P<SEMI_COLON>\;)                                      # semicolon operator
| (?P<DOT>\.)                                             # dot 
| (?P<PLUS>\+)                                            # plus
| (?P<IDENTIFIER>[A-Za-z_]\w*)                            # identifiers and keywords
| (?P<FLOAT>\d+\.\d+)                                     # float numbers
| (?P<INTEGER>\d+)                                        # integer numbers
| (?P<STRING>"(?:\\.|[^"\\])*")                           # double-quoted strings with escape support
| (?P<NEWLINE>\n)                                         # new line
"""

class TokenType(Enum):
    COMMENT = "COMMENT"
    K_FUNCTION = "K_FUNCTION"
    K_RETURN = "K_RETURN"
    K_PRINT = "K_PRINT"
    K_VAR = "K_VAR"
    OPEN_BRACE = "OPEN_BRACE"
    CLOSE_BRACE = "CLOSE_BRACE"
    OPEN_PARAM = "OPEN_PARAM"
    CLOSE_PARAM = "CLOSE_PARAM"
    SEMI_COLON = "SEMI_COLON"
    DOT = "DOT"
    PLUS = "PLUS"
    IDENTIFIER = "IDENTIFIER"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    STRING = "STRING"
    NEWLINE = "NEWLINE"
    K_EOF = "K_EOF"

class Word:
    def __init__(self, w_raw: str, w_type: TokenType, w_line: int, w_span: tuple[int, int]):
        self.raw = w_raw
        self.type = w_type
        self.line = w_line
        self.span = w_span

def tokenize(program: str):
    line = 1
    tokens = list()
    compiled_grammar = re.compile(TOKEN_GRAMMAR, re.VERBOSE)
    for item in compiled_grammar.finditer(program):
        token_type = TokenType[item.lastgroup]
        if token_type == TokenType.NEWLINE:
            line += 1
        elif token_type == TokenType.COMMENT:
            continue
        else:
            raw = item.group()
            token_span = (item.start(), item.end())
            tokens.append(Word(raw, cast(TokenType, token_type), line, token_span))
    tokens.append(Word("EOF", TokenType.K_EOF, 0, (0, 0)))
    return tokens