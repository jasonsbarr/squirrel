import jsons


class Environment:

    def __init__(self, parent=None, vars=None):
        self.parent = parent
        if vars is None:
            self.vars = {}
        else:
            self.vars = vars

    def extend(self):
        return Environment(parent=self)

    def lookup(self, name):
        scope = self
        while scope:
            if name in scope.vars:
                return scope
            scope = scope.parent
        return None

    def get(self, name):
        scope = self.lookup(name)
        if scope:
            return scope.vars[name]
        raise ReferenceError(f"{name} is not defined")

    def set(self, name, value):
        scope = self.lookup(name)

    def define(self, name, value):
        self.vars[name] = value
        return True

    def __str__(self):
        return jsons.dump(self)

    def __repr__(self):
        return f"Environment({self.parent}, {self.vars})"


def evaluate(ast):
    pos = 0
    child = ast.children[pos]

    def get_next_node():
        nonlocal pos
        pos += 1
        return ast.children[pos]

    def eval_expr(node):
        if node.type == "BinaryOperation":
            return apply_op(
                node.op, eval_expr(
                    node.left), eval_expr(
                    node.right))

        if node.type == "UnaryOperation":
            return apply_unary(node.op, eval_expr(node.expr))

        if node.type == "NumericLiteral":
            return node.value

    def apply_op(op, left, right):
        if op.value == "+":
            return left + right
        if op.value == "-":
            return left - right
        if op.value == "*":
            return left * right
        if op.value == "/":
            return left / right

    def apply_unary(op, expr):
        if op.value == "-":
            return -expr

    while pos < len(ast.children):
        current_value = eval_expr(child)

        try:
            child = get_next_node()
        except IndexError:
            return current_value
