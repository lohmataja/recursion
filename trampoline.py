# normal recursive factorial
def fact_recursive(n):
    return 1 if n <= 1 else n * fact_recursive(n-1)

# normal tail-recursive factorial
def fact_normal_tail_rec(n, accum):
    return accum if n <= 1 else fact_normal_tail_rec(n-1, accum*n)

# both blow up the stack
# print fact_recursive(100)
# print fact_normal_tail_rec(100, 1)
# print fact_recursive(1000) #raises RuntimeError: maximum recursion depth exceeded
# print fact_normal_tail_rec(1000, 1)

# normal mutual recursion
def even_recursive(n):
    return True if n == 0 else odd_recursive(n-1)

def odd_recursive(n):
    return False if n == 0 else even_recursive(n-1)

# normal mutual recursion blows the stack
# print even_recursive(100)
# print odd_recursive(50)
# print even_recursive(1000)
# print odd_recursive(1000)

# trampoline-ready recursive functions
def fact(n, accum):
    if n <= 1:
        return accum
    else:
        return lambda: fact(n-1, accum*n) #returns thunk instead of a call to itself

# trampoline-ready mutual recursion
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

# finally, the trampoline function
def tramp(f, *args, **kwargs):
    res = f(*args, **kwargs)
    while callable(res):
        res = res()
    return res

# trampolining recursive functions prevents stack overflows
# print tramp(fact, 1000, 1)
# print tramp(even, 1000)

# there is another way to define the trampoline function: it can accept the _result_ of calling f on *args:
def tramp_result(f):
    res = f
    while callable(res):
        res = res()
    return res

# this also works
# print tramp_result(fact(1000, 1))
# print tramp_result(odd(1000))

#now attempting to stick a trampoline into a generator
def bad_tramp(f):
   """
   takes a tail-recursive function f
   returns a trampolined version of this function
   """
   def tramp_f(*args, **kwargs):
       res = f(*args, **kwargs)
       while callable(res):
               res = res()
       return res
   return tramp_f

# there is nothing inherently bad with this decorator: it returns a working trampolined function
# tramped_fact = bad_tramp(fact)
# print tramped_fact(1000, 1)

#BUT if we use it to change the original function, the trouble begins...
#there are two ways of doing this: either using decorator syntax directly:

@bad_tramp
def bad_factorial(n, accum):
    return accum if n <= 1 else lambda: bad_factorial(n-1, accum*n) #same definition as fact
# print bad_factorial(1000, 1)

#or by doing what decorators are doing under the hood:
# fact = bad_tramp(fact)
# print fact(1000, 1) #raises RuntimeError: maximum recursion depth exceeded while calling a Python object
# different error from before (cf.: RuntimeError: maximum recursion depth exceeded)

# this behavior is caused by the fact that lambda: <...> doesn't close over any variables,
# so if we change the definition of fact in the process of creating a trampolined version of it, the new function fact
# will be calling the "new" version of itself, which will create new frames. Cf.:

# x = [lambda: i+1 for i in range(3)]
# print [j() for j in x] #[3, 3, 3] When this line is called, the value of i is read from the global environment
##way to go around it is to force the closure over i:
# x = [(lambda real_i: lambda: real_i+1)(i) for i in range(3)]
# print [j() for j in x] #[1, 2, 3]

#how can we take this idea and improve our decorator?
def better_tramp(f):
   """
   takes a tail-recursive function f
   returns a trampolined version of this function
   """
   def tramp_f(*args, **kwargs):
       res = f(*args, **kwargs)
       while callable(res):
               res = res()
       return res
   return tramp_f

@better_tramp
def better_factorial(n, accum):
    return accum if n <= 1 else (lambda real_f: lambda: real_f(n-1, accum*n))(better_factorial)
print better_factorial(1000, 1)

# a possible workaround to avoid name collision. Won't work with mutual recursion.
# def deco_tramp(f):
#    """
#    takes a tail-recursive function f
#    return a trampolined version of this function
#    """
#    f_itself = lambda *a,**kw: f(f_itself, *a, **kw)
#    def tramp_f(*args, **kwargs):
#        res = f_itself(*args, **kwargs)
#        while callable(res):
#            res = res()
#        return res
#    return tramp_f
#
# @deco_tramp
# def recur_deco_fact(recur, n, accum):
#     if n <= 1:
#         return accum
#     else:
#         return lambda: recur(n-1, accum*n)

# import sys
# sys.setrecursionlimit(4)