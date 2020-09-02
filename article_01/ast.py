class ASTNode:

    def __init__(self, node_type, start, end):
        self.type = node_type
        self.start = start
        self.end = end


class ProgramNode(ASTNode):

    def __init__(self, tokens):
        self.type = "Program"
        self.tokens = tokens
        self.start = {"line": tokens[0].line, "col": tokens[0].start}
        self.end = {"line": tokens[-1].line, "col": tokens[-1].end}
        self.children = []

    def __repr__(self):
        return f"ProgramNode({self.tokens})"

    def __str__(self):
        return f"{self.type}, children: {self.children}"


class NumberNode(ASTNode):

    def __init__(self, value, start, end):
        super().__init__("NumericLiteral", start, end)
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value}, {self.start}, {self.end})"
