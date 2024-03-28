"""
@Author : SakuraFox
@Time: 2024-03-28 22:17
@File : demo100.py
@Description : SEIR模型演示
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 总人数
N = 1000
# 感染率
beta = 0.4
# 疾病潜伏期
Te = 14
# 恢复率
gamma = 0.1

# 感染者
I = 10
# 潜伏者
E = 0
# 恢复者
R = 0
# 易感染人群
S = N - I - E - R
# 传播时间
T = 150

# 初始值
INI = [S, E, I, R]  # S, E, I, R


# 定义SEIR方程
def funcSEIR(inivalue, _):
    y = np.zeros(4)
    X = inivalue
    # 易感个体变化
    y[0] = -(beta * X[0] * X[2]) / N
    # 潜伏个体变化
    y[1] = (beta * X[0] * X[2]) / N - X[1] / Te
    # 感染个体变化
    y[2] = X[1] / Te - gamma * X[2]
    # 治愈个体变化
    y[3] = gamma * X[2]
    return y


# 时间范围
T_range = np.arange(0, T + 1)

# 求解模型
RES = odeint(funcSEIR, INI, T_range)

# 可视化
plt.figure(figsize=(12, 8))
plt.plot(RES[:, 0], color='darkblue', label='Susceptible', marker='.')
plt.plot(RES[:, 1], color='orange', label='Exposed', marker='.')
plt.plot(RES[:, 2], color='red', label='Infection', marker='.')
plt.plot(RES[:, 3], color='green', label='Recovery', marker='.')

plt.title('SEIR Model')
plt.legend()
plt.xlabel('Day')
plt.ylabel('Population')
plt.show()
