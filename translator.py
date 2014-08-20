__author__ = 'Liuda'
import ast, inspect

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
    def visit_FunctionDef(self, node):
