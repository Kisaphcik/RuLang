class ExpressionNode:
    pass


class StatementNode(ExpressionNode):
    def __init__(self):
        self.__codeString = []

    def addNode(self, node: ExpressionNode):
        self.__codeString.append(node)

    @property
    def codeString(self):
        return self.__codeString


class VarNode(ExpressionNode):
    def __init__(self, value):
        self.value = value


class NumNode(ExpressionNode):
    def __init__(self, value):
        self.value = value


class StringNode(ExpressionNode):
    def __init__(self, value):
        self.value = value


class FuncNode(ExpressionNode):
    def __init__(self, operator, operands):
        self.operator = operator
        self.value = operands
