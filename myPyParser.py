import myPyTokens as Tokens
import myPyAST as AST

class Parser:
    def __init__(self, tokensList):
        self.__pos = 0
        self.__tokensList = tokensList
        self.__stack = dict()
        self.__parse()
        self.__run()

    def __match(self, *tokens):
        if self.__pos < len(self.__tokensList):
            currentToken = self.__tokensList[self.__pos]
            if currentToken.type in tokens:
                self.__pos += 1
                return currentToken
        return None

    def __require(self, *tokens):
        token = self.__match(*tokens)
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
        raise Exception("Ошибка")

    def __parseVarOrNum(self):
        cheak = self.__match(Tokens.TokensEnum.VAR)
        if cheak != None:
           return AST.VarNode(cheak.value)
        cheak = self.__match(Tokens.TokensEnum.NUM)
        if cheak != None:
            return AST.NumNode(cheak.value)
        cheak = self.__match(Tokens.TokensEnum.STRING)
        if cheak != None:
            return AST.StringNode(cheak.value)
        cheak = self.__match(Tokens.TokensEnum.FUNC)
        if cheak != None:
            self.__pos -= 1
            return self.__parseExpression()
        cheak = self.__match(Tokens.TokensEnum.LFIPAR)
        if cheak != None:
            root = AST.StatementNode()
            while not self.__match(Tokens.TokensEnum.RFIPAR):
                bodyString = self.__parseExpression()
                self.__require(Tokens.TokensEnum.SEMICOLON)
                root.addNode(bodyString)
            self.__pos -= 1
            self.__require(Tokens.TokensEnum.RFIPAR)
            return root
        raise SyntaxError("Ожидался ввод цифры или переменной")

    def __run(self):
        for i in self.__root.codeString:
            self.__expr(i)

    def __expr(self, node):
        if isinstance(node, AST.FuncNode):
            if node.operator == "вывод":
                print(" ".join([str(self.__expr(i)) for i in node.value]))
            elif node.operator == "создать":
                self.__stack[node.value[0].value] = None
                return node.value[0].value
            elif node.operator == "присвоить":
                self.__stack[node.value[0].value] = self.__expr(node.value[1])
                return None
            elif node.operator == "сложить":
                if isinstance(node.value[0], AST.NumNode):
                    return self.__summator([self.__expr(i) for i in node.value])
                else:
                    return "".join([self.__expr(i) for i in node.value])
            elif node.operator == "вычесть":
                return self.__minuser([self.__expr(i) for i in node.value])
            elif node.operator == "умножить":
                return self.__multiplier([self.__expr(i) for i in node.value])
            elif node.operator == "разделить":
                return self.__divisier([self.__expr(i) for i in node.value])
            elif node.operator == "целчислДел":
                return self.__expr(node.value[0]) // self.__expr(node.value[1])
            elif node.operator == "степень":
                return self.__expr(node.value[0]) ** self.__expr(node.value[1])
            elif node.operator == "корень":
                return self.__expr(node.value[0]) ** (1 / self.__expr(node.value[1]))
            elif node.operator == "инк":
                self.__stack[node.value[0].value] = self.__expr(node.value[0]) + 1
                return self.__stack[node.value[0].value]
            elif node.operator == "дек":
                self.__stack[node.value[0].value] = self.__expr(node.value[0]) - 1
                return self.__stack[node.value[0].value]
            elif node.operator == "ввод":
                self.__stack[node.value[0].value] = input(self.__expr(node.value[1]) if len(node.value) > 1 else "")
                return self.__stack[node.value[0].value]
            elif node.operator == "вЦелЧис":
                return int(self.__expr(node.value[0]))
            elif node.operator == "вПлавЧис":
                return float(self.__expr(node.value[0]))
            elif node.operator == "вСтроку":
                return str(self.__expr(node.value[0]))
            elif node.operator == "вБул":
                return bool(self.__expr(node.value[0]))
            elif node.operator == "если":
                if self.__expr(node.value[0]):
                    self.__expr(node.value[1])
                else:
                    if len(node.value) == 3:
                        self.__expr(node.value[2])
        elif isinstance(node, AST.VarNode):
            return self.__stack[node.value]
        elif isinstance(node, AST.StringNode):
            return node.value[1:-1]
        elif isinstance(node, AST.NumNode):
            return int(node.value)
        elif isinstance(node, AST.StatementNode):
            for k in node.codeString:
                self.__expr(k)

    @staticmethod
    def __summator(arr: list):
        res = 0
        for i in arr:
            res += i
        return res

    @staticmethod
    def __minuser(arr: list):
        res = arr[0]
        for i in arr[1:]:
            res -= i
        return res

    @staticmethod
    def __multiplier(arr: list):
        res = arr[0]
        for i in arr[1:]:
            res *= i
        return res

    @staticmethod
    def __divisier(arr: list):
        res = arr[0]
        for i in arr[1:]:
            res /= i
        return res