
func = lambda x: print(x)


def fc(x):
    return print(x)

print(fc(2))

# def cube(x):
#     print(x**3)
#     return x**3
#
#
# a = 2
# a2 = square(a)
# a6 = cube(a2)
#
# print(a6)


def num_factors(num):
    count = 0
    for i in range(1, num+1):
        if num % i == 0:
            count += 1
    return count


l = [1, 2, 3, 4, 5, 6]
# output4 = [False, True, True, False, True, False]

# output = list(map(num_factors, l))

# output2 = map(lambda x: x**2, output)

output3 = list(
    filter(
        lambda x: num_factors(x) == 2,      # Filtering machine
        l                                   # Things to filter
    )
)

output4 = list(
    map(
        lambda x: num_factors(x) == 2,      # Mapper
        l                                   # Input to map
    )
)

output5 = list(
    filter(
        lambda x: x,
        output4
    )
)

# print(list(output))
print(output3)
print(output4)
print(output5)

# for i in range(3):
#     print(next(output2))
# print(output)

# num_factor_list = []
# for num in l:
#     num_factor_list.append(num_factors(num))

# print(num_factor_list)

# from functools import reduce
#
# reduce(fn, iterable, init_value)
#
# countri = [country+ " " +str(sale) for country, sale in zip(countries, sales)]
# print([[i+j for i in "abc"] for j in "def"])

# Recursion
# def printer(n):
#     if n <= 0:
#         return 1
#     else:
#         print(n)
#         printer(n - 1)
# printer(5)
# def printer(n):
#     if n == 0:
#         print(1)
#     else:
#         printer(n-1)
#         print(n)
# printer(5)

# def tribo(n):
#     if n == 1:
#         return 0
#     elif n == 2 or n == 3:
#         return 1
#     else:
#         return tribo(n-1) + tribo(n-2) + tribo(n-3)
#
#
# result = tribo(6)
# print(result)

# def checker(n):
#    if len(n) == 1:
#       print("Yes")
#    elif n[len(n) - 1] == n[0]:
#       checker(n.lstrip(n[0]).rstrip(n[len(n) - 1]))
#    else:
#       print("No")
#
# checker("madam")
# checker("noob")

# def fact(n):
#     if n == 0:
#         print("Factorial of 0 is 1")
#         return 1
#     elif n < 0:
#         print("Factorial doesn't exist for negative numbers")
#     else:
#         result = n * fact(n-1)
#         print(result)
#         return result
#
# fact(5)

# def permutate(lst, f=0):
#     if f >= len(lst):
#         print(lst)
#         return
#     for s in range(f, len(lst)):
#         lst[f], lst[s] = lst[s], lst[f]
#         permutate(lst, f+1)
#         lst[f], lst[s] = lst[s], lst[f]
#
#
# permutate([1, 2, 3])