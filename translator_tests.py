__author__ = 'Liuda'
import ast, inspect
import translator


def rec_fact(n):
    if n <= 1:
        return 1
    else:
        return n * rec_fact(n-1)

def tail_fact(n, accum=1):
    if n <= 1:
        return accum
    else:
        return tail_fact(n-1, accum * n)

def f(n):
    print(n)
    f = 5
    return f

def sq(x):
    return x*x

def sum_squares(x):
    if x <= 1:
        return sq(x)
    else:
        return sq(x) + sum_squares(x-1)

def print_n_squares(x):
    print(sq(x))
    if x > 1:
        print_n_squares(x-1)

print(translator.isRecursive(ast.parse('a = 5 + 9')))

def test():
    for func in [rec_fact, tail_fact, f, sq, sum_squares, print_n_squares]:
        tree = ast.parse(inspect.getsource(func))
        print(func.__name__, translator.isRecursive(tree))

test()