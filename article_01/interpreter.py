def evaluate(ast):
    pos = 0
    child = ast.children[pos]

    def get_next_child():
        nonlocal pos
        pos += 1
        return ast.children[pos]

    def eval_expr(node):
        if node.type == "NumericLiteral":
            return node.value

    while pos < len(ast.children):
        current_value = eval_expr(child)

        try:
            child = get_next_child()
        except IndexError:
            return current_value
