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

class InfoGatherer(ast.NodeVisitor):
    """
    traverses the tree, storing the function name, default value and recursive calls.
    """
    def __init__(self):
        self.name = None
        self.default_value = None
        self.recursive_returns = []

    def is_recursive(self, tree):
        for node in ast.walk(tree):
            if type(node).__name__ == 'Call' and node.func.id == self.name:
                return True
        return False

    def find_recursive_returns(self, tree):
        return [node for node in ast.walk(tree) if type(node).__name__ == 'Return' and self.is_recursive(node)]

    def visit_FunctionDef(self, node):
        self.name = node.name
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Return(self, node):
        if not self.is_recursive(node):
            self.default_value = node.value
        else: #recursive return
            self.recursive_returns.append(node)

# class RecCallToAccum(ast.NodeTransformer):
#     def __init__(self, name):
#         self.name = name
#     def visit_Call(self, node):
#         if type(node).__name__ == 'Call' and node.func.id == self.name:
#             return make_name('accum')
#
# class RecursionTranslator(ast.NodeTransformer):
#     default_value = 1
#
#     def make_Name(self, name):
#         return ast.Name(
#             id=name,
#             ctx=ast.Param()
#         )
#
#     def make_Num(self, x):
#         return ast.Num(n=x)
#
#     def visit_FunctionDef(self, node):
#         node.args.args.append(self.make_Name('accum'))
#         node.args.defaults.append(self.make_Num(self.default_value))
#         print(node.args.args)
#         print(node.args.defaults)
#         return node


def tail_fact(n, accum=1):
    if n <= 1: return accum
    else: return tail_fact(n - 1, accum * n)

def rec_fact(n):
    if n <= 1:
        return 1
    else:
        return n * rec_fact(n-1)

ig = InfoGatherer()
tree = ast.parse(inspect.getsource(rec_fact))
ig.visit(tree)
print(ig.name)
print(ig.default_value.n)
for r in ig.recursive_returns:
    print polish(ast.dump(r))
# print(ast.dump(tree))
# print(polish(ast.dump(tree)))