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
        func = self.__match(Tokens.TokensEnum.FUNC)
        if func != None:
            self.__pos -= 1
            return self.__parseExpression()
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
                return self.__summator([self.__expr(i) for i in node.value])
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
        elif isinstance(node, AST.VarNode):
            return self.__stack[node.value]
        elif isinstance(node, AST.StringNode):
            return node.value[1:-1]
        elif isinstance(node, AST.NumNode):
            return int(node.value)

    @property
    def Nodes(self):
        return self.__root

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