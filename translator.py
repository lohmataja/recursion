__author__ = 'Liuda'
import ast, inspect, imp
from ast_pretty_printer import print_ast
import sys

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

def is_recursive(tree, name):
    """
    Takes a tree and returns a recursive ast.Call if one is present in the tree, otherwise None.
    """
    for node in ast.walk(tree):
        if type(node).__name__ == 'Call' and node.func.id == name:
            return True
    return False

class InfoGatherer(ast.NodeVisitor):
    """
    traverses the tree, storing the function name, default value and recursive calls.
    """
    def __init__(self):
        self.name = None
        self.default_value = None
        self.recursive_returns = []

    # def find_recursive_returns(self, tree):
    #     return [node for node in ast.walk(tree) if type(node).__name__ == 'Return' and self.is_recursive(node)]

    def visit_FunctionDef(self, node):
        self.name = node.name
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Return(self, node):
        rec_call = is_recursive(node, self.name)
        if rec_call:
            self.recursive_returns.append(node)
        else:
            self.default_value = node.value

class Mangler(ast.NodeTransformer):
    """
    Requirements to the ast tree passed:
    tree should be a result of ast.parse on a recursive function that has one base case, one recursive call per recursive return
    and no internal function definitions.
    """
    def __init__(self, tree):
        ig = InfoGatherer()
        ig.visit(tree)
        self.name = ig.name
        self.default_value = ig.default_value
        self.recursive_returns = ig.recursive_returns

    def make_Name(self, name, ctx_val):
        return ast.Name(
            id=name,
            ctx=ctx_val
        )

    def make_Num(self, x):
        return ast.Num(n=x)

    def update_recursive_calls(self):
        for node in self.recursive_returns:
            self.visit_Return(node)

    def visit_Return(self, node):
        if is_recursive(node, self.name):
            #substitute the recursive call with accum, store the call in self.outer
            ast.NodeTransformer.generic_visit(self, node)
            print_ast(node)
            print_ast(self.outer)
            self.outer.args.append(node.value)
            print_ast(self.outer)
            return ast.Return(value=self.outer)
        else:
            return ast.Return(value=self.make_Name('accum', ast.Load()))

    def visit_Call(self, node):
        if node.func.id == self.name:
            # print 'Visiting Call'
            # print_ast(node)
            self.outer = node
            return self.make_Name('accum', ast.Load())
        else:
            return node

    def visit_FunctionDef(self, node):
        #update arguments
        node.args.args.append(self.make_Name('accum', ast.Param()))
        node.args.defaults.append(self.default_value)
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Print(self, node):
        return node

def tail_fact(n, accum=1):
    if n <= 1: return accum
    else: return tail_fact(n - 1, accum * n)

def rec_fact(n):
    if n <= 1:
        return 1
    else:
        return n * rec_fact(n-1)


(filename,) = sys.argv[1:]
tree = ast.parse(open(filename, 'r').read())

m = Mangler(tree)
m.visit(tree)
print_ast(tree)

ast.fix_missing_locations(tree)
code = compile(tree, filename, "exec")

namespace = imp.new_module(filename)
eval(code, namespace.__dict__)