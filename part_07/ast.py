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

    # Name parameter so it can be processed as either a binary or assignment
    # operation
    def __init__(self, type, left, op, right):
        super().__init__(type)
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"{self.type}: {self.left} {self.op} {self.right}"

    def __repr__(self):
        return f"BinaryOpNode({self.type}, {self.left}, {self.op}, {self.right})"


class UnaryOpNode(ASTNode):

    def __init__(self, op, expr):
        super().__init__("UnaryOperation")
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"UnaryOp: {self.op} {self.expr}"

    def __repr__(self):
        return f"UnaryOpNode({self.op}, {self.expr})"


class IdentifierNode(ASTNode):

    def __init__(self, name):
        super().__init__("Identifier")
        self.name = name

    def __str__(self):
        return f"Identifier: {self.name}"

    def __repr__(self):
        return f"Identifier({self.name})"


class CallExpressionNode(ASTNode):

    def __init__(self, name, args=None):
        super().__init__("CallExpression")
        self.name = name

        if args is None:
            self.args = []
        else:
            self.args = args

    def __str__(self):
        return f"Call expr function name: {self.name}, args: {self.args}"

    def __repr__(self):
        return f"CallExpressionNode({self.name}, {self.args})"


class VariableDeclarationNode(ASTNode):

    def __init__(self, var_name, expr):
        super().__init__("VariableDeclaration")
        self.var_name = var_name
        self.expr = expr

    def __str__(self):
        return f"Variable declaration: {self.var_name} given {self.expr}"

    def __repr__(self):
        return f"VariableDeclarationNode({self.var_name}, {self.expr})"


class BooleanNode(ASTNode):
    def __init__(self, value):
        super().__init__("BooleanLiteral")
        self.value = True if value == "true" else False

    def __str__(self):
        return f"Boolean: {self.value}"

    def __repr__(self):
        return f"BooleanNode({str(self.value).lower()})"


class NilNode(ASTNode):

    def __init__(self):
        super().__init__("NilLiteral")
        self.value = None

    def __str__(self):
        return "Nil"

    def __repr__(self):
        return "NilNode()"


class ConditionalNode(ASTNode):

    def __init__(self, cond, then, elseExpr):
        super().__init__("ConditionalExpression")
        self.cond = cond
        self.then = then
        self.elseExpr = elseExpr

    def __repr__(self):
        return f"ConditionalNode({self.cond}, {self.then}, {self.elseExpr})"
