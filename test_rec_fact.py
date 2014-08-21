def fact(n):
    if n <= 1:
        return 1
    else:
        return n * fact(n - 1)

print(fact(10))

def sq(x):
    return x * x

def sum_squares(n):
    if n <= 1:
        return 1
    else:
        return sq(n) * sum_squares(n - 1)

print sum_squares(10)  # 13168189440000

def two_even_three_odd(n):
    if n == 1:
        return 3
    elif n == 2:
        return 4
    elif n % 2 == 0:
        return 2 * n + two_even_three_odd(n-1)
    else:
        return 3 * n + two_even_three_odd(n-1)

print(two_even_three_odd(10)) #132