# 统计学-计算标准得分
import math


def get_score(x, u, q, n):
    return round(abs((x - u)) / q * math.sqrt(n), 3)


list1 = [61.2, 62.6, 40.1, 51.7, 38.0, 59.8,
         47.6, 47.7, 56.3, 35.0]
list2 = [83.0, 93.7, 82.1, 72.4, 92.3,
         68.7, 76.5, 88.4, 79.6, 63.3]
list3 = [50]
list4 = [0.949, 4.332, 0.664, 2.403, 3.89, 3.573, 1.107, 2.656, 0.126, 5.281]
list5 = [3.542, 3.984, 3.131, 0.538, 3.795, 3.099, 0.759, 0.727, 1.992, 4.743]
result = []
for qq in list1:
    result.append(get_score(50, qq, 10, 10))
# print(result)
# list4相加
sum1 = 0
sum2 = 0
for n in list4:
    sum1 += n
for n in list5:
    sum2 += n
print(sum1, sum2)
