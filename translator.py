__author__ = 'Liuda'
import ast, inspect
from ast_pretty_printer import polish

def isRecursive(tree):
    try:
        #get function name and function definition subtree
        for node in ast.walk(tree):
            if type(node).__name__ == 'FunctionDef':
                name = node.name
                func_def = node
        for node in ast.walk(func_def): #find whether this func_def contains recursive calls
            if type(node).__name__ == 'Call' and node.func.id == name:
                return True
        return False
    except UnboundLocalError:
        print('No functions found')
        return False

class RecursionTranslator(ast.NodeTransformer):
    default_value = 1

    def make_Name(self, name):
        return ast.Name(
            id=name,
            ctx=ast.Param()
        )

    def make_Num(self, x):
        return ast.Num(n=x)

    def visit_FunctionDef(self, node):
        node.args.args.append(self.make_Name('accum'))
        node.args.defaults.append(self.make_Num(self.default_value))
        print(node.args.args)
        print(node.args.defaults)
        return node


def tail_fact(n, accum=1):
    if n <= 1:
        return accum
    else:
        return tail_fact(n - 1, accum * n)

def rec_fact(n):
    if n <= 1:
        return 1
    else:
        return n * rec_fact(n-1)

rt = RecursionTranslator()
tree = ast.parse(inspect.getsource(rec_fact))
rt.visit(tree)
print(ast.dump(tree))
print(polish(ast.dump(tree)))