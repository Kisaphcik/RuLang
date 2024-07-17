import re
import myPyTokens as Tokens

class Lexer:
    def __init__(self, code):
        self.__code = code
        self.__pos = 0
        self.__tokensList = []
        self.__lexingCode()

    def __lexingCode(self):
        while self.__nextTokens():
            pass

    def __nextTokens(self):
        if self.__pos >= len(self.__code):
            return False
        for typeToken in Tokens.TokensEnum.getTypes():
            regex = re.compile('^' + typeToken.regex)
            result = re.match(regex, self.__code[self.__pos::])
            if result and result[0]:
                if not typeToken is Tokens.TokensEnum.COMMENT and not typeToken is Tokens.TokensEnum.SPACE:
                    self.__tokensList.append(Tokens.Token(typeToken, result[0], self.__pos))
                self.__pos += len(result[0])
                return True
        raise NameError("Вы написали несуществующий токен!")

    @property
    def tokensList(self):
        return self.__tokensList