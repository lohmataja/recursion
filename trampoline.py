from types import FunctionType
def even(n):
    if n == 0:
        return True
    else:
        return lambda: odd(n-1)

def odd(n):
    if n == 0:
        return False
    else:
        return lambda: even(n-1)

##def tramp(f):
##    """
##    takes a tail-recursitve function f
##    return a trampolined version of this function
##    """
##    def tramp_f(*args, **kwargs):
##        res = f(*args, **kwargs)
##        while True:
##            if type(res) == FunctionType:
##                res = res()
##            else:
##                return res
##    return tramp_f
##
##@tramp
def tramp(f, *args, **kwargs):
    res = f(*args, **kwargs)
    while True:
        if type(res) == FunctionType:
            res = res()
        else:
            return res
def fact_iter(n, accum):
    if n <= 1:
        return accum
    else:
        return lambda: fact_iter(n-1, accum*n)
#what I need is a trampoline decorator!
    
print tramp(fact_iter, 5, 1)
