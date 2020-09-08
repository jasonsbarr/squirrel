def sum(*args):
    s = 0
    for arg in args:
        s += arg
    return s


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    return x / y


def pow(base, exp):
    return base ** exp


def typeof(obj):
    if type(obj).__name__ == "int" or type(obj).__name__ == "Decimal":
        return "Number"
    if type(obj).__name__ == "bool":
        return "Boolean"
    if type(obj).__name__ == "NoneType":
        return "Nil"


def str_upcase(s):
    return s.upper()


def str_downcase(s):
    return s.lower()


def str_slice(s, start, end):
    return s[start:end]


def str_len(s):
    return len(s)


def str_index(s, i):
    return s[i]


def str_reverse(s):
    return s[::-1]
