import re

# Token types as constants
NUMBER, EOF = "NUMBER", "EOF"


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"{self.type} token, value: {self.value}"

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class InputException(Exception):

    def __init__(self, message):
        super().__init__(message)


class InputStream:

    def __init__(self, input):
        self.input = input
        self.pos = -1

    def next(self):
        """Get next char from input and advance position"""
        self.pos += 1

        try:
            char = self.input[self.pos]
        except IndexError:
            char = ""

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
        raise InputException(f"{msg}")


# Helper functions
def is_digit(char):
    return bool(re.match(r"\d", char))


def is_number(string):
    return bool(re.match(r"^\d+\.?\d*$", string))


def is_whitespace(char):
    return bool(re.match(r"\s", char))


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
        has_dot = False
        num = read_while(lambda char: is_digit(char) or char == ".")

        if "." in num:
            has_dot = True

        if num.count(".") > 1 or not is_number(num):
            input.die(f"Invalid Number constant {num}")

        if has_dot:
            tokens.append(
                Token(
                    NUMBER,
                    float(num)))
        else:
            tokens.append(
                Token(
                    NUMBER,
                    int(num)))

    # While there is input, create tokens based on the current character
    while input.pos < len(input.input):
        if is_whitespace(current):
            # Skip whitespace
            read_while(is_whitespace)
        elif is_digit(current):
            read_number()
        else:
            input.die(f"Unknown input '{current}'")

    # Add the final EOF token to signal the end of input
    tokens.append(Token(EOF, None))

    return tokens
