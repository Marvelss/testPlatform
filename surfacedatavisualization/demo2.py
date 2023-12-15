# 自定义有效区域,并自动补全为方阵
import math

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from tqdm import tqdm
from PIL import Image

# 自定义区域范围
min_row, max_row, min_col, max_col = 38, 60, 71, 100

use_col_list = []
sideLength = max_col - min_col - max_row + min_row
use_min_row, use_max_row = min_row - sideLength / 2, max_row + sideLength / 2
print('间距上下扩展数值')
print(sideLength)
print('------------------------------------')
print('扩展后最大最小行')
print(use_min_row, use_max_row)
for i in range(min_col, max_col + 1):
    use_col_list.append(i)
print('------------------------------------')
print('y轴列')
print(use_col_list)

df1 = pd.read_excel('2266s.xlsx',
                    header=None,
                    skiprows=int(use_min_row),
                    nrows=int(use_max_row - use_min_row),
                    usecols=use_col_list)
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

print('------------------------------------')
print('x轴刻度')
y_label = []
num = min_row
for _ in range(len(ax.get_xticklabels())):
    y_label.append(num)
    num += 2
print(y_label)
# 打印x轴标签
# print()
ax.set_yticklabels(y_label)
f.savefig(('14.png'), dpi=500, bbox_inches='tight')
