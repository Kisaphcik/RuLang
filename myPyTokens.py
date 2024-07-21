import dataclasses

class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos


@dataclasses.dataclass
class TokenType:
    name: str
    regex: str

class TokensEnum:
    COMMENT = TokenType("COMMENT", "//[ \\t\\rа-яА-ЯA-Za-z0-9!`<>~@#$%^&|№;%:?,.\\+\\-]*")
    STRING = TokenType("STRING", "\"[ \\n\\t\\rа-яА-Я0-9A-Za-z!`<>~@#$%^&|№;%:?,.\\+\\-]*\"")
    FUNC = TokenType("FUNC", "[а-яА-ЯA-Za-z]*\\(")
    VAR = TokenType("VAR", "[а-яА-Я]*")
    NUM = TokenType("NUM", "[0-9]*")
    SEMICOLON = TokenType("SEMICOLON", ";")
    LPAR = TokenType("LPAR", "\\(")
    RPAR = TokenType("RPAR", "\\)")
    SPACE = TokenType("SPACE", "[ \\n\\t\\r]")
    COMMA = TokenType("COMMA", ",")
    START = TokenType("START", "\\начало")
    END = TokenType("END", "\\конец")

    @classmethod
    def getTypes(cls):
        return [cls.COMMENT, cls.START, cls.END, cls.STRING, cls.FUNC, cls.VAR, cls.NUM, cls.SEMICOLON, cls.LPAR, cls.RPAR, cls.SPACE, cls.COMMA]