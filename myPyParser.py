import myPyTokens as Tokens
import myPyAST as AST

class Parser:
    def __init__(self, tokensList):
        self.__pos = 0
        self.__tokensList = tokensList
        self.__parse()

    def __match(self, *tokens):
        if self.__pos < len(self.__tokensList):
            currentToken = self.__tokensList[self.__pos]
            if currentToken.type in list(map(lambda x: x, tokens[0] if isinstance(tokens[0], tuple) else tokens)):
                self.__pos += 1
                return currentToken
        return None

    def __require(self, *tokens):
        token = self.__match(tokens)
        if (not token):
            raise SyntaxError(f"На позиции {self.__pos} ожидался токен(ы) {list(map(lambda x: x.name, tokens))}")
        return tokens[0]

    def __parse(self):
        self.__root = AST.StatementNode()
        while self.__pos < len(self.__tokensList):
            codeStringNode = self.__parseExpression()
            self.__require(Tokens.TokensEnum.SEMICOLON)
            self.__root.addNode(codeStringNode)

    def __parseExpression(self):
        operator = self.__match(Tokens.TokensEnum.FUNC)
        if operator:
            value = []
            while True:
                value.append(self.__parseVarOrNum())
                if not self.__match(Tokens.TokensEnum.COMMA):
                    break
            self.__require(Tokens.TokensEnum.RPAR)
            return AST.FuncNode(operator.value[:-1], value)
        raise Exception("Error")

    def __parseVarOrNum(self):
        var = self.__match(Tokens.TokensEnum.VAR)
        if var != None:
           return AST.VarNode(var.value)
        num = self.__match(Tokens.TokensEnum.NUM)
        if num != None:
            return AST.NumNode(num.value)
        string = self.__match(Tokens.TokensEnum.STRING)
        if string != None:
            return AST.StringNode(string.value)
        raise SyntaxError("Ожидался ввод цифры или переменной")


    @property
    def Nodes(self):
        return self.__root