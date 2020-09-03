import re

# Token types as constants
NUMBER, EOF, OPERATOR = "NUMBER", "EOF", "OPERATOR"

OPERATORS = ("+", "-", "*", "/", "%")


class Token:

    def __init__(self, type, value, line, start, end):
        self.type = type
        self.value = value
        self.line = line
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.type} token, value: {self.value}"

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.start}, {self.end})"


class InputException(Exception):

    def __init__(self, message):
        super().__init__(message)


class InputStream:

    def __init__(self, input):
        self.input = input
        self.pos = -1
        self.line = 1
        self.col = 0

    def next(self):
        """Get next char from input and advance position"""
        self.pos += 1

        try:
            char = self.input[self.pos]
        except IndexError:
            char = ""

        if char == "\n":
            self.line += 1
            self.col = 0
        else:
            self.col += 1

        return char

    def peek(self):
        """Get value of character at current pos"""
        try:
            char = self.input[self.pos]
        except IndexError:
            char = ""

        return char

    def eof(self):
        """Create EOF token when reach end of input"""
        return self.pos > len(self.input) - 1

    def die(self, msg):
        """Raise an exception on bad input"""
        raise InputException(f"{msg} at ({self.line}:{self.col})")


# Helper functions
def is_digit(char):
    return bool(re.match(r"\d", char))


def is_number(string):
    return bool(re.match(r"^\d+\.?\d*$", string))


def is_whitespace(char):
    return bool(re.match(r"\s", char))


def is_operator(string):
    return string in OPERATORS


def is_op_char(char):
    return char in "".join(OPERATORS)


# The main lexer function
def tokenize(input: InputStream) -> list:
    current = input.next()
    tokens = []

    def read_while(predicate):
        """Take in multiple characters while a condition is met"""
        nonlocal current
        s = ""
        while(not input.eof() and predicate(input.peek())):
            s += current
            current = input.next()
        return s

    def read_number():
        """Create number token from int or float literal"""
        nonlocal tokens, current
        start = input.col
        has_dot = False
        num = read_while(lambda char: not is_whitespace(char))

        if "." in num:
            has_dot = True

        if num.count(".") > 1 or not is_number(num):
            input.die(f"Invalid Number constant {num}")

        if has_dot:
            tokens.append(
                Token(
                    NUMBER,
                    float(num),
                    input.line,
                    start,
                    input.col))
        else:
            tokens.append(
                Token(
                    NUMBER,
                    int(num),
                    input.line,
                    start,
                    input.col))

    def read_operator():
        nonlocal tokens
        op = read_while(is_op_char)
        if not is_operator(op):
            input.die(f"Unknown symbol {op}")
        tokens.append(
            Token(
                OPERATOR,
                op,
                input.line,
                input.col,
                input.col + 1))

    # While there is input, create tokens based on the current character
    while input.pos < len(input.input):
        if is_whitespace(current):
            # Skip whitespace
            read_while(is_whitespace)
        elif is_digit(current):
            read_number()
        elif is_op_char(current):
            read_operator()
        else:
            input.die(f"Unknown input '{current}'")

    # Add the final EOF token to signal the end of input
    tokens.append(Token(EOF, None, input.line, input.col, input.col))

    return tokens
