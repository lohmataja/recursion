import ast, inspect

class AltDump(ast.NodeVisitor):

    def visit(self, node):
        res = []
        res.append(type(node).__name__+'(')
        field_values = []
        for field, value in ast.iter_fields(node):
            if type(value) == list:
                field_values.append(field+'=['+ ', '.join([self.visit(item) for item in value])+']')
            elif isinstance(value, ast.AST):
                field_values.append(field+'='+self.visit(value))
            # elif value == None:
            #     field_values.append(field+'=None')
            else:
                field_values.append(field+'='+ ("'{}'".format(value) if type(value) == str
                                    else str(value)))
        res.append(', '.join(field_values))
        self.generic_visit(node)
        res.append(')')
        return ''.join(map(str, res))

class Pretty(ast.NodeVisitor):
    def __init__(self, filler="  "):
        self.res = ''
        self.level = -1
        self.filler = filler
        self.out = []

    @property
    def prefix(self):
        return self.level * self.filler

    def visit(self, node):
        self.level +=1
        print(node)
        self.out.append(type(node).__name__ +'(')
        self.level += 1
        for field, value in ast.iter_fields(node):
            print(field, value)
            self.out.append(self.prefix+field)
            if type(value) == list and len(value) > 0:
                self.out.append('=[\n')
                for n in value:
                    self.visit(n)
                    # self.out.append(self.prefix+type(n).__name__ +'(\n')
                    # for child in ast.iter_child_nodes(n):
                    #     self.visit(child)
                self.out.append('=\n')
            elif isinstance(value, ast.AST):
                self.out.append('=')
                self.generic_visit(value)
            else:
                self.out.append('=' + str(value) + '\n')
        self.level -= 2

    def visit_Name(self, node):
        print("I'm here!")
        self.level += 1
        self.out.append(self.prefix + ast.dump(node))
        self.level -= 1

class PrettyPrinter(ast.NodeVisitor):
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

def polish(dump, prefix='\t'):
    new_str = []
    level = 0
    for i in range(len(dump)):
        if dump[i] == '(':
            level += 1
            new_str.append('('+('\n'+prefix*level)*(dump[i+1] != ')'))

        elif dump[i] == '[':
            level += 1
            new_str.append('['+('\n'+prefix*level)*(dump[i+1] != ']'))

        elif dump[i] == ',':
            new_str.append(',\n'+prefix*level)

        elif dump[i] == ')' or dump[i] == ']':
            level -= 1
            new_str.append(dump[i])
        elif dump[i] == ' ':
            continue

        else:
            new_str.append(dump[i])
    return ''.join(new_str)

def print_ast(tree, prefix='  '):
    print(polish(ast.dump(tree), prefix))

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

# tree = ast.parse(inspect.getsource(f))
# d = Pretty()
# tree = ast.parse(open('./test.py', 'r').read())
# print(ast.dump(tree))
tree = ast.parse(inspect.getsource(rec_fact))
# tree = ast.parse("a = 5")
a = AltDump()
my_dump = a.visit(tree)
# print(''.join(a.res))
py_dump = ast.dump(tree)
print my_dump
print(py_dump)
# d.visit(tree)
# print(''.join(d.out))
# print_ast(tree, '  ')
# print(ast.dump(ast.parse(inspect.getsource(rec_fact))))
# d.visit(ast.parse(inspect.getsource(tail_fact)))
# print(ast.dump(ast.parse(inspect.getsource(tail_fact))))
# d.visit(tree)

# v = PrettyPrinter()
# v.visit(tree)
