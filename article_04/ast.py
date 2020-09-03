class ASTNode:

    def __init__(self, node_type):
        self.type = node_type


class ProgramNode(ASTNode):

    def __init__(self):
        self.children = []
        super().__init__("Program")

    def __repr__(self):
        return f"ProgramNode()"

    def __str__(self):
        return f"{self.type}, children: {self.children}"


class NumberNode(ASTNode):

    def __init__(self, value):
        super().__init__("NumericLiteral")
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"


class BinaryOpNode(ASTNode):

    def __init__(self, left, op, right):
        super().__init__("BinaryOperation")
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp: {self.left} {self.op} {self.right}"

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op}, {self.right})"


class UnaryOpNode(ASTNode):

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"UnaryOp: {self.op} {self.expr}"

    def __repr__(self):
        return f"UnaryOpNode({self.op}, {self.expr})"
