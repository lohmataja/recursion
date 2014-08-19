import ast, inspect

class DecorativePrinter(ast.NodeVisitor):
    def __init__(self):
        self.res = ''
        self.level = -1

    def generic_visit(self, node):
        print(self.prefix+type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    @property
    def prefix(self):
        return self.level * '\t'

    def visit(self, node):
        def gen_visit_deco(f):
            def new_visit(*args, **kwargs):
                # self = args[0]
                self.level += 1
                f(*args, **kwargs)
                self.level -= 1
            return new_visit
        try:
            # method = getattr(self, "visit_{}".format(node.__class__.__name__)) #what's the difference betw. .__class__ vs. type()?
            method = getattr(self, "visit_{}".format(type(node).__name__))
        except AttributeError:
            method = self.generic_visit
        gen_visit_deco(method)(node)

    def visit_FunctionDef(self, node):
        print(self.prefix + type(node).__name__ +': '+ node.name)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_arguments(self, node):
        print(self.prefix + type(node).__name__ +': ')
        for field in node._fields:
            list_to_visit = getattr(node, field)
            if list_to_visit:
                print(self.prefix + field + ': ')
                for item in list_to_visit:
                    self.level += 1
                    ast.NodeVisitor.visit(self, item)
                    self.level -= 1

    def visit_arg(self, node):
        print(self.prefix + node.arg)

    def visit_Name(self, node):
        print(self.prefix+ node.id)

    def visit_Num(self, node):
        print(self.prefix+'Num:' + str(node.__dict__['n']))

    def visit_Str(self, node):
        print(self.prefix+'Str:' + node.s)

    def visit_Print(self, node):
        print(self.prefix+'Print:')
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        print(self.prefix+'Assign:')
        ast.NodeVisitor.visit(self, node)

    def visit_Expr(self, node):
        print(self.prefix+'Expr:')
        ast.NodeVisitor.generic_visit(self, node)

# def f(n, accum=1):
#     if n <= 1:
#         return accum
#     else:
#         return f(n - 1, accum * n)
#
#
# tree = ast.parse(inspect.getsource(f))

tree = ast.parse(open('./test.py', 'r').read())
print(ast.dump(tree))

d = DecorativePrinter()
d.visit(tree)

# v = PrettyPrinter()
# v.visit(tree)

# u = UglyPrinter()
# res = u.visit(tree)
# u.pretty_print(res)
