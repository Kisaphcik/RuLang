class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos


class TokenType:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex


class TokensEnum:
    COMMENT = TokenType("COMMENT", "//[ \\t\\rа-яА-Я0-9!`<>~@#$%^&|№;%:?,.]*")
    STRING = TokenType("STRING", "\"[ \\n\\t\\rа-яА-Я0-9!`<>~@#$%^&|№;%:?,.]*\"")
    FUNC = TokenType("FUNC", "[а-яА-Я]*\\(")
    VAR = TokenType("VAR", "[а-яА-Я]*")
    NUM = TokenType("NUM", "[0-9]*")
    SEMICOLON = TokenType("SEMICOLON", ";")
    LPAR = TokenType("LPAR", "\\(")
    RPAR = TokenType("RPAR", "\\)")
    SPACE = TokenType("SPACE", "[ \\n\\t\\r]")
    COMMA = TokenType("COMMA", ",")
    LFIPAR = TokenType("LPAR", "\\{")
    RFIPAR = TokenType("RPAR", "\\}")
    IFCMD = TokenType("RPAR", "if(")

    @classmethod
    def getTypes(cls):
        return [cls.COMMENT, cls.STRING, cls.FUNC, cls.VAR, cls.NUM, cls.SEMICOLON, cls.LPAR, cls.RPAR, cls.SPACE, cls.COMMA, cls.LFIPAR, cls.RFIPAR]