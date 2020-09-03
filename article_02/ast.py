class Point:

    def __init__(self, line, col):
        self.line = line
        self.col = col

    def __str__(self):
        return f"({self.line}:{self.col})"

    def __repr__(self):
        return f"Point({self.line}, {self.col})"


class ASTNode:

    def __init__(self, node_type, start, end):
        self.type = node_type
        self.start = start
        self.end = end


class ProgramNode(ASTNode):

    def __init__(self, tokens):
        self.tokens = tokens
        self.children = []
        super().__init__("Program", Point(tokens[0].line, tokens[0].start), Point(
            tokens[-1].line, tokens[-1].end))

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
