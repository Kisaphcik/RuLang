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
    STRING = TokenType("STRING", "\"[а-яА-Я]*\"")
    FUNC = TokenType("FUNC", "[а-яА-Я]*\\(")
    VAR = TokenType("VAR", "[а-яА-Я]*")
    NUM = TokenType("NUM", "[0-9]*")
    SEMICOLON = TokenType("SEMICOLON", ";")
    LPAR = TokenType("LPAR", "\\(")
    RPAR = TokenType("RPAR", "\\)")
    QUOTE = TokenType("RPAR", "\"")
    SPACE = TokenType("SPACE", "[ \\n\\t\\r]")
    COMMA = TokenType("COMMA", ",")

    @classmethod
    def getTypes(cls):
        return [cls.STRING, cls.FUNC, cls.VAR, cls.NUM, cls.SEMICOLON, cls.LPAR, cls.RPAR, cls.QUOTE, cls.SPACE, cls.COMMA]