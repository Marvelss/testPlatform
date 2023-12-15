# 获取最大有效区域
import math

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from tqdm import tqdm
from PIL import Image

min_row, max_row, min_col, max_col = 0, 0, 0, 0
data = pd.read_excel('2266s.xlsx', header=None)
# 定义一个空数组，用于存储出现非1数值的行数
rows_with_non_one_values = []

# 遍历每一行内容
for index, row in data.iterrows():
    # 检查每个单元格的数值是否为1
    if any(row != 1):
        # 如果有非1的数值，则将该行数添加到数组中
        rows_with_non_one_values.append(index)

# 打印包含非1数值的行数数组
print("包含非1数值的行数数组:")
print(rows_with_non_one_values)
print(rows_with_non_one_values[0] + 1, rows_with_non_one_values[-1] + 1)

# 定义一个空数组，用于存储出现非1数值的列数
columns_with_non_one_values = []

# 遍历每一列内容
for column in data.columns:
    # 检查每个单元格的数值是否为1
    if any(data[column] != 1):
        # print(data[column].head(59))
        # 如果有非1的数值，则将该列数添加到数组中
        columns_with_non_one_values.append(column)

# 打印包含非1数值的列数数组
print("包含非1数值的列数数组:")
print(columns_with_non_one_values[0], columns_with_non_one_values[-1])
# 最大最小行列
min_row = rows_with_non_one_values[0] + 1
max_row = rows_with_non_one_values[-1] + 1
min_col = columns_with_non_one_values[0]
max_col = columns_with_non_one_values[-1]

# 实际热力图的行列
print(min_row, max_row)
print(columns_with_non_one_values)
fillLength = max(max_row - min_row, max_col - min_col)
print(fillLength)
df1 = pd.read_excel('2266s.xlsx',
                    header=None,
                    skiprows=min_row,
                    nrows=fillLength,
                    usecols=columns_with_non_one_values)
# df.to_excel('a1.xlsx')
# plt.xticks(5, 31)
f, ax = plt.subplots(1, 1)
# df12 = pd.read_excel('a1.xlsx')
sns.heatmap(df1, cmap='RdYlGn_r', linewidths=0.1,
            vmin=0, vmax=1)
# 设置Axes的标题
ax.set_title('Group: Day Of Years:')
# ax.set_yticks([5, 10, 10, 31, 10])
# 获取x轴标签
# x_labels = [label.get_text() for label in ax.get_xticklabels()]

print('----')
print(math.ceil(fillLength/len(ax.get_xticklabels())))
y_label = []
num = min_row
for _ in range(len(ax.get_xticklabels())):
    y_label.append(num)
    num += 2
print(y_label)
# 打印x轴标签
# print()
ax.set_yticklabels(y_label)
f.savefig(('1.png'), dpi=500, bbox_inches='tight')
