import sys

from lark import Lark, Transformer


pewer_parser = Lark(r"""
    ?exp: SIGNED_NUMBER  -> number
        | string
        | "true"         -> true
        | "false"        -> false

    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='exp')


class TreeToPyObject(Transformer):
    def string(self, s):
        (s,) = s
        return s[1:-1]
    def number(self, n):
        (n,) = n
        return float(n)

    true = lambda self, _: True
    false = lambda self, _: False


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        text = f.read()

    tree = pewer_parser.parse(text)
    print(TreeToPyObject().transform(tree))
