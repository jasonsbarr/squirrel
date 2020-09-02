import re

# Token types as constants
NUMBER, EOF = "NUMBER", "EOF"


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
        char = self.input[self.pos]

        if char == "\n":
            self.line += 1
            self.col = 0

        return char

    def peek(self):
        """Get value of character at current pos"""
        return self.input[self.pos]

    def eof(self):
        """Create EOF token when reach end of input"""
        return Token(EOF, None, self.line, self.col, self.col)

    def die(self, msg):
        """Raise an exception on bad input"""
        raise InputException(f"{msg} at ({self.line}:{self.col})")


def lexer(input: InputStream) -> list:
    current = ""
    tokens = []

    def advance():
        nonlocal tokens

        try:
            current = input.next()
        except IndexError:
            tokens.append(input.eof())


def is_digit(char):
    return bool(re.match("[0-9]", char))
