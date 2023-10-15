# data science
# 0123456789
# n n n n n n

def add_string(str1):
    length = len(str1)
    if length > 2:
        if str1[-3:] == 'ing':
            str1 += 'ly'
        else: str1 += 'ing'
    return str1

str1 = input()
print(add_string(str1))





# def are_parenthesis_balanced(seq):
#     def is_balanced(s, idx=0, open_count=0):
#         if idx == len(s):
#             return open_count == 0
#
#         if s[idx] == '(':
#             return is_balanced(s, idx + 1, open_count + 1)
#         elif s[idx] == ')' and open_count > 0:
#             return is_balanced(s, idx + 1, open_count - 1)
#         else:
#             return False
#
#     return [is_balanced(s) for s in seq]



            # # def max_subarray_sum(arr):
#     duplicate = arr.copy()
#     n = []
#     for i in range(len(duplicate)): #max till now , current sum
#         for j in range(len(duplicate)):
#             m = duplicate
#             if sum(m) > sum(n):
#                 n = m[:]
#             duplicate.pop(0)
#     # for i in range(len(arr)):
#     #     for j in range(len(arr)):
#     #         q = arr
#     #         if sum(q) > sum(n):
#     #             n = q[:]
#     #         print(arr, sum(arr))
#     #         arr.pop(0).pop(len(arr) - 1)
#     print(n)
# max_subarray_sum([1, -2, 3, 4, -5, 8])


# def find_largest(lst):
#     if len(lst) == 1:
#         return lst[0]
#     else:
#         n = len(lst)
#         max_of_left_subarry = find_largest(lst[:n//2])
#         max_of_right_subarry = find_largest(lst[n//2:])
#         return max(max_of_left_subarry, max_of_right_subarry)
#
# print(find_largest([3, 4, 2, 10, 44, 21]))
#