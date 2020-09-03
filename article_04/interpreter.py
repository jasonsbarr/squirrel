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

    while pos < len(ast.children):
        current_value = eval_expr(child)

        try:
            child = get_next_node()
        except IndexError:
            return current_value
