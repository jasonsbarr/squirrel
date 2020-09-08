from ast import ProgramNode, NumberNode, BinaryOpNode, UnaryOpNode, IdentifierNode, CallExpressionNode, VariableDeclarationNode, BooleanNode, NilNode, ConditionalNode, LambdaNode
from lexer import InputStream, tokenize


PRECEDENCE = {
    "=": 1,
    "||": 3,
    "&&": 4,
    "<": 6, ">": 6, "<=": 6, ">=": 6,
    "==": 6, "!=": 6, "is": 6,
    "+": 8, "-": 8,
    "*": 10, "/": 10, "%": 10
}


def parse(tokens):
    pos = 0
    token = tokens[pos]

    def get_next_token():
        nonlocal pos, token
        if not token.type == "EOF":
            pos += 1
            token = tokens[pos]

    def lookahead():
        if not token.type == "EOF":
            return tokens[pos + 1]
        else:
            return token

    def parse_program():
        ast = ProgramNode()
        while not token.type == "EOF":
            ast.children.append(parse_expr())
            get_next_token()
        return ast

    def parse_expr():
        if token.type == "KEYWORD":
            return parse_keyword()
        if token.type == "NUMBER" or token.type == "BOOLEAN" or token.type == "NIL":
            return maybe_binary(parse_atom(), 0)
        if token.type == "IDENTIFIER":
            return maybe_call()
        if token.value == "(":
            return maybe_binary(parse_atom(), 0)
        if token.type == "OPERATOR":
            return parse_atom()
        raise SyntaxError(f"Unknown token: {token}")

    def parse_keyword():
        if token.value == "def":
            return parse_variable_declaration()
        if token.value == "if":
            return parse_if()
        if token.value == "lambda":
            return parse_lambda()

    def parse_call(name_token):
        args = []
        # Skip opening paren
        get_next_token()
        while token.value != ")":
            if token.value != ",":
                args.append(parse_expr())
            get_next_token()
        # Skip closing paren
        get_next_token()
        return CallExpressionNode(name_token.value, args)

    def parse_variable_declaration():
        # Skip def to get variable name
        get_next_token()
        var_name_token = token
        next_tok = lookahead()
        if next_tok.value == "(":
            # skip opening paren
            get_next_token()
            get_next_token()
            params = []
            if token.type == "IDENTIFIER":
                while token.value != ")":
                    if token.value != ",":
                        params.append(parse_expr())
                    get_next_token()
            # skip closing paren
            get_next_token()
            body = parse_expr()
            expr = LambdaNode(params, body)
        else:
            expr = maybe_binary(parse_atom(), 0)
        return VariableDeclarationNode(var_name_token.value, expr)

    def parse_if():
        # get if expr
        get_next_token()
        cond = parse_expr()
        # skip then keyword
        get_next_token()
        get_next_token()
        then = parse_expr()
        get_next_token()
        if (token.value == "else"):
            get_next_token()
            else_expr = parse_expr()
        else:
            else_expr = None
        return ConditionalNode(cond, then, else_expr)

    def parse_lambda():
        # skip lambda keyword token
        get_next_token()
        # skip opening paren
        get_next_token()
        params = []
        if token.type == "IDENTIFIER":
            while token.value != ")":
                if token.value != ",":
                    params.append(parse_expr())
                get_next_token()
        # skip closing paren
        get_next_token()
        body = parse_expr()
        return LambdaNode(params, body)

    def parse_atom():
        if token.type == "OPERATOR":
            op = token
            get_next_token()
            return UnaryOpNode(op, parse_atom())
        if token.type == "NUMBER":
            return NumberNode(
                token.value)
        if token.type == "BOOLEAN":
            return BooleanNode(token.value)
        if token.type == "NIL":
            return NilNode()
        if token.value == "(":
            get_next_token()
            node = parse_expr()
            # Needed to skip closing paren since parse_factor was advancing pos
            get_next_token()
            return maybe_binary(node, 0)
        if token.type == "IDENTIFIER":
            return IdentifierNode(token.value)

    def maybe_binary(left, my_prec=0):
        next = lookahead()
        if next.type == "OPERATOR":
            get_next_token()
            precedence = PRECEDENCE[token.value]
            if precedence > my_prec:
                get_next_token()
                right = maybe_binary(parse_expr(), precedence)
                binary = BinaryOpNode(
                    "AssignmentOperation" if next.value == "=" else "BinaryOperation",
                    left,
                    next,
                    right)
                return maybe_binary(binary, my_prec)
        return left

    def maybe_call():
        name_token = token
        next = lookahead()
        if next.value == "(":
            get_next_token()
            return parse_call(name_token)
        return maybe_binary(parse_atom(), 0)

    return parse_program()
