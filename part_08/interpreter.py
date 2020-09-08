import jsons

import stdlib


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
        if scope:
            scope.vars[name] = value
            return value
        raise ReferenceError(f"{name} is not defined")

    def define(self, name, value):
        if name in self.vars:
            raise ReferenceError(f"{name} is already defined")
        self.vars[name] = value
        return True

    def __str__(self):
        return str(jsons.dump(self))

    def __repr__(self):
        return f"Environment({self.parent}, {self.vars})"


globalVars = {}

for key, value in vars(stdlib).items():
    if "__" not in key:
        globalVars[key] = value

globalEnv = Environment(vars=globalVars)


def evaluate(ast, env=globalEnv):
    pos = 0
    child = ast.children[pos]

    def get_next_node():
        nonlocal pos
        pos += 1
        return ast.children[pos]

    def eval_expr(node, env: Environment):
        if node.type == "LambdaExpression":
            return make_lambda(node, env)
        if node.type == "ConditionalExpression":
            return apply_if(node, env)
        if node.type == "AssignmentOperation":
            return apply_assignment(node, env)
        if node.type == "VariableDeclaration":
            return apply_declaration(node, env)
        if node.type == "BinaryOperation":
            return apply_op(
                node.op, eval_expr(
                    node.left, env), eval_expr(
                    node.right, env))
        if node.type == "UnaryOperation":
            return apply_unary(node.op, eval_expr(node.expr, env))
        if node.type == "NumericLiteral":
            return node.value
        if node.type == "BooleanLiteral":
            return node.value
        if node.type == "NilLiteral":
            return None
        if node.type == "Identifier":
            return env.get(node.name)
        if node.type == "CallExpression":
            return apply_call(node, env)

    def apply_op(op, left, right):
        if op.value == "+":
            return left + right
        if op.value == "-":
            return left - right
        if op.value == "*":
            return left * right
        if op.value == "/":
            return left / right
        if op.value == "%":
            return left % right
        if op.value == "==":
            return left == right
        if op.value == "&&":
            return left and right
        if op.value == "||":
            return left or right
        if op.value == "!=":
            return left != right
        if op.value == "<":
            return left < right
        if op.value == ">":
            return left > right
        if op.value == ">=":
            return left >= right
        if op.value == "<=":
            return left <= right
        if op.value == "is":
            return left is right

    def apply_unary(op, expr):
        if op.value == "-":
            return -expr
        if op.value == "!":
            return not expr

    def apply_call(node, env):
        fn = env.get(node.name)
        args = [eval_expr(arg, env) for arg in node.args]
        return fn(*args)

    def apply_declaration(node, env):
        env.define(node.var_name, None)
        return eval_expr(node.expr, env)

    def apply_assignment(node, env):
        return env.set(node.left.name, eval_expr(node.right, env))

    def apply_if(node, env):
        cond = eval_expr(node.cond, env)
        if cond:
            return eval_expr(node.then, env)
        elif node.elseExpr:
            return eval_expr(node.elseExpr, env)

    def make_lambda(node, env):
        def new_function(*args):
            scope = env.extend()
            for param, arg in zip(node.params, args):
                scope.define(param.name, arg)
            return eval_expr(node.body, scope)
        return new_function

    while pos < len(ast.children):
        current_value = eval_expr(child, env)

        try:
            child = get_next_node()
        except IndexError:
            return current_value
