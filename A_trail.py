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
# #     for i in range(row):
# #         for j in range(column):
# #             ans_mat[j][i] = matrix[i][j]
# #             print(ans_mat)
# #     return ans_mat
# #
# #
# # def transpose1(matrix):
# #     m, n = len(matrix), len(matrix[0])
# #     transposed = [[0] * m for _ in range(n)]
# #     for i in range(m):
# #         for j in range(n):
# #             transposed[j][i] = matrix[i][j]
# #     return transposed
# #
# # print(transpose([[1,2,3],[4,5,6]]))
# # # print(transpose1([[1,2,3],[4,5,6]]))
#
# def add(a, b):
#     """
#     Return the sum of two numbers.
#
#     Examples:
#     >>> add(2, 3)
#     5
#     >>> add(-1, 1)
#     0
#     >>> add(2.5, 0.5)
#     3.0
#     >>> 1/3  # doctest: +ELLIPSIS
#     0.333...
#     >>> 1/0  # doctest: +SKIP
#     0.333
#     """
#     return a + b
#
#
# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
import datetime
import random
import time


# def generate_random_number():
#     # 设置目标时间为20:05
#     target_hour, target_minute = 15, 00
#
#     while True:
#         # 获取当前系统时间
#         current_time = datetime.datetime.now().time()
#
#         # 定义人物字典
#         people_mapping = {1: '王海波', 2: '易焕东', 3: '尤康林', 4: '李晨光', 5: '张壮志', 6: '纪雷',7: '王智英',8: '陈建光'}
#
#         # 检查是否当前时间等于20:00
#         if True: #current_time.hour == target_hour and current_time.minute == target_minute:
#             # 生成1到6之间的随机数
#             random_number = random.randint(1, 8)
#
#             # 根据随机数获取对应的人物
#             person = people_mapping.get(random_number)
#
#             print(f"当前时间: {current_time}, 吉时已到，随机选中的英雄是: {person}")
#             return
#         else:
#             print(f"当前时间: {current_time}, 等待中...")
#             # 每隔0.1秒查询一次
#             time.sleep(0.1)
#
# generate_random_number()


# import numpy as np
# import random
# import glob
# import pandas as pd
#
#
# def fit_plane_and_calculate_thickness(points):
#     """
#     对点云进行平面拟合，并计算厚度（中间95%的点在法向方向上的极差）
#
#     :param points: N×3 的 NumPy 数组，每行是 (x, y, z) 坐标
#     :return: (plane_normal, plane_d, thickness)
#     """
#     # 1. 计算点云中心
#     centroid = np.mean(points, axis=0)
#
#     # 2. 计算去中心化坐标
#     centered_points = points - centroid
#
#     # 3. SVD 分解，找到法向量
#     _, _, vh = np.linalg.svd(centered_points)
#     plane_normal = vh[-1]  # 右奇异向量的最后一列，即法向量 (a, b, c)
#
#     # 4. 计算平面方程 ax + by + cz + d = 0 其中 d = -dot(n, centroid)
#     plane_d = -np.dot(plane_normal, centroid)
#
#     # 5. 计算每个点到拟合平面的距离
#     distances = np.abs(np.dot(points, plane_normal) + plane_d) / np.linalg.norm(plane_normal)
#
#     # 6. 计算中间 95% 的极差
#     lower_bound, upper_bound = np.percentile(distances, [2.5, 97.5])
#     thickness = upper_bound - lower_bound
#
#     return plane_normal, plane_d, thickness
#
#
# # ==================== 测试代码 ====================
# if __name__ == "__main__":
#
#     dir = r'\\10.69.31.10\BenchMarking\TestData\RS-Airy\hesai_test\picth\senarios\JT128\ground\*.csv'
#     dirs = glob.glob(dir)
#     print(dirs)
#     dfs = []
#     for csv in dirs:
#         df_ = pd.read_csv(csv)
#         dfs.append(df_)
#     df_re = pd.concat(dfs)
#     x = df_re['x(m)']
#     y = df_re['y(m)']
#     z = df_re['z(m)']
#
#     point_cloud = np.vstack((x, y, z)).T  # N×3 矩阵
#     print(point_cloud)
#
#     normal, d, thickness = fit_plane_and_calculate_thickness(point_cloud)
#
#     print(f"拟合平面法向量: {normal}")
#     print(f"拟合平面方程: {normal[0]:.3f}x + {normal[1]:.3f}y + {normal[2]:.3f}z + {d:.3f} = 0")
#     print(f"计算出的厚度: {thickness:.3f}")

#
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
#
#
# def fft_spectrum(signal):
#     """
#     计算信号的 FFT 频谱
#     :param signal: 输入信号
#     :return: 频率, 频谱幅值
#     """
#     fft_vals = np.fft.fft(signal)  # 计算FFT
#     freqs = np.fft.fftfreq(len(signal))  # 计算对应的频率
#     return freqs[:len(freqs) // 2], np.abs(fft_vals)[:len(fft_vals) // 2]  # 只取正频部分
#
#
# def estimate_smoothing(signal, threshold=0.2):
#     """
#     判断信号是否经过平滑滤波
#     :param signal: 目标信号
#     :param threshold: 高频能量占比阈值
#     :return: 是否可能被平滑 (True / False)
#     """
#     freqs, fft_vals = fft_spectrum(signal)
#
#     # 计算高频能量占比（取最高 50% 频率部分）
#     total_energy = np.sum(fft_vals)
#     high_freq_energy = np.sum(fft_vals[len(fft_vals) // 2:])  # 高频部分
#     high_freq_ratio = high_freq_energy / total_energy
#
#     print(f"高频能量占比: {high_freq_ratio:.3f}")
#
#     return high_freq_ratio  # 如果高频能量低于阈值，可能经过平滑滤波
#
#
# # 生成测试信号
# # np.random.seed(42)
# # original_signal = np.random.normal(0, 1, 1000)  # 原始随机噪声
# # smoothed_signal = np.convolve(original_signal, np.ones(10) / 10, mode='same')  # 进行均值平滑
#
# df_QT = np.array(pd.read_csv(r'\\10.69.31.10\BenchMarking\TestData\RS-Airy\hesai_test\picth\senarios\RSA\QT_d.csv')['Dist(m)'])
# df_XT = np.array(pd.read_csv(r'\\10.69.31.10\BenchMarking\TestData\RS-Airy\hesai_test\picth\senarios\RSA\XT_d.csv')['Dist(m)'])
# df_RSA = np.array(pd.read_csv(r'\\10.69.31.10\BenchMarking\TestData\RS-Airy\hesai_test\picth\senarios\RSA\RSA_d.csv')[' distance_m'])
# print(df_RSA)
#
#
# # 仅检查 smoothed_signal
# # print("该信号是否被平滑:", estimate_smoothing(signal))
#
# # 绘制频谱
# # freqs, orig_fft = fft_spectrum(signal)
# freqs_Q, smoothed_fft_Q = fft_spectrum(df_QT)
# freqs_X, smoothed_fft_X = fft_spectrum(df_XT)
# freqs_R, smoothed_fft_R = fft_spectrum(df_RSA)
#
# # plt.plot(freqs, orig_fft, label="原始信号频谱", linestyle="dotted")
# plt.plot(freqs_Q, smoothed_fft_Q, label=f"QT Spectrum {estimate_smoothing(df_QT):.4f}", linestyle="solid")
# plt.plot(freqs_X, smoothed_fft_X, label=f"XT Spectrum {estimate_smoothing(df_XT):.4f}", linestyle="--")
# plt.plot(freqs_R, smoothed_fft_R, label=f"RT Spectrum {estimate_smoothing(df_RSA):.4f}", linestyle="-.")
#
#
# plt.legend()
# plt.show()
#
# import glob
#
# import pandas as pd
#
# csv_dirs = glob.glob(r'\\172.20.2.21\ft\TestData\ISO测评数据\20250416_ISO抗干扰\ATX-BYD-PR3301-0037\1.0m同向干扰\*.csv')
# dfs = []
# for csv_dir in csv_dirs:
#     df = pd.read_csv(csv_dir)
#     dfs.append(df)
# df_re = pd.concat(dfs)
# print(df_re)
# print(len(df_re))
# S = (120000 * 100 - len(df_re)) / (120000 * 100)
# print(S)
#
# #

# this means nothing

# Let us add another


from a_sign import a_fun
a_fun()
