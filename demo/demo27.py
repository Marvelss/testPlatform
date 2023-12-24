import numpy as np
from scipy import optimize
import statsmodels.api as sm

import pandas as pd

# 方法一:使用最小二乘法拟合直线的方法

fire = pd.read_excel('test.xlsx', header=None)
# x = np.array([60, 63, 72, 83, 67, 98, 85,
#               61, 71, 80, 93, 72, 72, 71, 62, 50])
# y = np.array([74, 80, 97, 81, 72, 110, 96,
#               76, 86, 87, 88, 87, 83, 91, 73, 64])


x = fire.iloc[:, 0]
print(list(x))
y = fire.iloc[:, 1]
print(list(y))


def regula(p):
    a, b = p
    return y - a - b * x


result = optimize.least_squares(regula, [0, 0])
print('方法一：回归参数β0和β1的估计值分别为：', result.x)
# 方法二：使用statsmodels库中regression模块的linear_model子模块创建OLS类
X = sm.add_constant(x)
model = sm.OLS(y, X)
results = model.fit()
# print('方法二：回归参数β0和β1的估计值分别为：', results.params)

print(results.summary())
# 提取F-statistic
print(results.fvalue)

# 提取F-statistic 的pvalue
print(results.f_pvalue)
