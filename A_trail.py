# def threeSum(nums):
#     re = []
#     for i in range(len(nums) - 2):
#         for j in range(i + 1, len(nums) - 1):
#             for k in range(j + 1, len(nums)):
#                 if i != j and i != k and j != k and nums[i] + nums[j] + nums[k] == 0:
#                     re.append([nums[i], nums[j], nums[k]])
#     print(re)
#     print('================')
#     re2 = []
#     if len(re) > 0:
#         re2.append(re[0])
#         for l in range(1, len(re)):
#             li = []
#             same = False
#             for tru in re2:
#                 if set(tru) == set(re[l]):
#                     same = True
#             if not same:
#                 li.append(tru)
#
#             print('li', li)
#             re2 = re2 + li
#             print('re2', re2)
#
#     return re2
#
# nums = [3,0,-2,-1,1,2]
# print(threeSum(nums))
#
# def merge(nums1, m, nums2, n):
#     """
#     Do not return anything, modify nums1 in-place instead.
#     """
#     for i in range(n):
#         nums1.pop()
#     nums1 = nums1 + nums2
#     nums1.sort()
#     print(nums1)
#
#
# merge([1,2,3,0,0,0], 3, [2,5,6], 3)

# def shuffle(nums, n):
#     """
#     :type nums: List[int]
#     :type n: int
#     :rtype: List[int]
#     """
#     ans_list = list()
#     for i in range(n):
#         print(i * 2, i * 2 + 1, i, i + n)
#         ans_list[i * 2], ans_list[i * 2 + 1] = nums[i], nums[i + n]
#         print(ans_list)
#     return ans_list
#
# shuffle([2,5,1,3,4,7], 3)

#
# def transpose(matrix):
#     """
#     :type matrix: List[List[int]]
#     :rtype: List[List[int]]
#     """
#     row = len(matrix)
#     column = len(matrix[0])
#     ans_mat = [[0] * row] * column
#     ans_mat = [[0] * row for _ in range(column)]
#     print(ans_mat)
#     for i in range(row):
#         for j in range(column):
#             ans_mat[j][i] = matrix[i][j]
#             print(ans_mat)
#     return ans_mat
#
#
# def transpose1(matrix):
#     m, n = len(matrix), len(matrix[0])
#     transposed = [[0] * m for _ in range(n)]
#     for i in range(m):
#         for j in range(n):
#             transposed[j][i] = matrix[i][j]
#     return transposed
#
# print(transpose([[1,2,3],[4,5,6]]))
# # print(transpose1([[1,2,3],[4,5,6]]))

def add(a, b):
    """
    Return the sum of two numbers.

    Examples:
    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    >>> add(2.5, 0.5)
    3.0
    >>> 1/3  # doctest: +ELLIPSIS
    0.333...
    >>> 1/0  # doctest: +SKIP
    0.333
    """
    return a + b


if __name__ == "__main__":
    import doctest
    doctest.testmod()
