import sys
import imp
import ast
import inspect


(filename,) = sys.argv[1:]

tree = ast.parse(open(filename, 'r').read())


def tramp_deco(f):
    def trampo(*args, **kwargs):
        res = f(*args, **kwargs)
        while callable(res):
            res = res()
        return res
    return trampo

tramp_ast = ast.parse(inspect.getsource(tramp_deco)).body[0]


class NameChanger(ast.NodeTransformer):
    def __init__(self, name):
        self.name = name

    def visit_Name(self, el):
        if el.id == self.name:
            el.id = "_{}".format(self.name)
        return el


class AutoLambda(ast.NodeTransformer):

    def visit_FunctionDef(self, el):
        nc = NameChanger(el.name)
        nc.visit(el)
        el.name = "_{}".format(el.name)

        self.generic_visit(el)
        return el

    def visit_Return(self, el):
        el.value = ast.Lambda(
            args=ast.arguments(
                args=[],
                varargs=None,
                kwargs=None,
                kwonlyargs=[],
                defaults=[],
                kw_defaults=[],
            ),
            body=el.value
        )
        return el


traverse = AutoLambda()
traverse.visit(tree)

tree.body.insert(0, tramp_ast)

newbody = []
for statement in tree.body:
    newbody.append(statement)

    if isinstance(statement, ast.FunctionDef):
        name = statement.name
        if name.startswith("_"):
            newbody.append(ast.parse(
                "{} = tramp_deco({})".format(
                    name[1:], name
                )
            ).body[0])

tree.body = newbody

ast.fix_missing_locations(tree)
code = compile(tree, filename, "exec")

namespace = imp.new_module(filename)
eval(code, namespace.__dict__)
