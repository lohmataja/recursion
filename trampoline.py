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

def fact_iter(n, accum):
    if n <= 1:
        return accum
    else:
        return lambda: fact_iter(n-1, accum*n)

def tramp(f, *args, **kwargs):
    res = f(*args, **kwargs)
    while True:
        if callable(res):
            res = res()
        else:
            return res

def deco_tramp(f):
   """
   takes a tail-recursitve function f
   return a trampolined version of this function
   """
   def tramp_f(*args, **kwargs):
       res = f(*args, **kwargs)
       while True:
           if callable(res):
               res = res()
           else:
               return res
   return tramp_f

@deco_tramp
def deco_fact(n, accum):
    if n <= 1:
        return accum
    else:
        return lambda: deco_fact(n-1, accum*n)
#tests for regular trampoline
# print tramp(fact_iter(500, 1))
# print tramp(even(1000))

#tests for decorator trampoline, which doesn't work
# print deco_fact(1000, 1)
