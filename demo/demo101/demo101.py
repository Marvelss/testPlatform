"""
@Author : SakuraFox
@Time: 2024-03-29 17:15
@File : demo101.py
@Description : SEIR病害动态模型测试(可行)
"""
import pandas as pd

from fitness2 import fitness2

yzqPath = '晚稻移栽期.xlsx'
zbPath = r'E:\a_python\program\testPlatform\demo\demo101\训练集.xlsx'
metPath = '气象数据.xlsx'
jizhiPath = '预测峰值.xlsx'

# 移摘期
YZQ_num = pd.read_excel(yzqPath, sheet_name='HN', usecols=[2, 3, 4], header=None)
YZQ_txt = pd.read_excel(yzqPath, sheet_name='HN', usecols=[0, 1], header=None)
YZQ_data = pd.read_excel(yzqPath, sheet_name='HN', header=None)
# print(YZQ_num)
# 训练集
ZB_num = pd.read_excel(zbPath, sheet_name='HN', header=None)
# print(ZB_num)
ZB_data = ZB_num
# 气象数据
met_num = pd.read_excel(metPath, sheet_name='HN', usecols=[2, 3, 4, 5], header=None)

met_txt = pd.read_excel(metPath, sheet_name='HN', usecols=[0, 1], header=None)
met_data = pd.read_excel(metPath, sheet_name='HN', header=None)
# 预测峰值
Jizhi_num = pd.read_excel(jizhiPath, sheet_name='训练集HN', header=None)
Jizhi_data = pd.read_excel(jizhiPath, sheet_name='训练集HN', header=None)

RMSE, D = fitness2(2, 0.2, 40, 60, 15, 15,
                YZQ_num, YZQ_txt,
                YZQ_data, ZB_num, ZB_data, met_num,
                met_txt, met_data, Jizhi_num, Jizhi_data)
output_list = []
for arr in D:
    output_list.append(arr.tolist()[0][0])

# 预测病害结果
print(output_list)
# RMSE
print(RMSE)
#
# ka = 4
# kb = 0.1
# kc = 30
# q = 50
# r = 40
# OPT_PRI = 40
# RMSE = fitness2(float(ka),
#                 float(kb),
#                 float(kc), float(q),
#                 float(r), float(OPT_PRI),
#                 YZQ_num, YZQ_txt,
#                 YZQ_data, ZB_num, ZB_data, met_num,
#                 met_txt, met_data, Jizhi_num, Jizhi_data)

