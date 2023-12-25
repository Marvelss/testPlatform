"""
@Author  : SakuraFox
@Time    : 2023-12-25 9:21
@File    : demo28.py
@Description : 马铃薯和石头分类
"""
import pickle

import cv2
import numpy as np
import pandas as pd
import os

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

potato_dir = 'potatoes'  # 土豆图像文件夹路径
stone_dir = 'stones'  # 石头图像文件夹路径

sum_profiles = []  # 特征
labels = []  # 标签

# 设置3个ROI区域,将图像划分为3个通道,每个通道可能包含土豆、石块或为空

for img_path in os.listdir(potato_dir):
    labels.append(0)  # 0表示土豆
    img = cv2.imread(os.path.join(potato_dir, img_path))
    height, width = img.shape[:2]
    roi_width = width // 2

    roi1 = img[:, :roi_width]
    roi2 = img[:, roi_width:2 * roi_width]
    roi3 = img[:, 2 * roi_width:]
    # 对每个ROI计算白色像素比例,判断该ROI是否包含目标
    threshold = 0.0001

    white_pixels2 = np.sum(roi2 > 250) / (roi_width * height)
    has_obj2 = white_pixels2 > threshold

    print(white_pixels2)
    sum_profile2 = []
    if not has_obj2:
        for row in roi2:
            sum_profile2.append(0)
    if has_obj2:
        for row in roi2:
            sum_profile2.append(round(np.sum(row)))
    sum_profiles.append(np.asarray(sum_profile2))

for img_path in os.listdir(stone_dir):
    labels.append(1)  # 1表示石头
    img = cv2.imread(os.path.join(stone_dir, img_path))
    height, width = img.shape[:2]
    roi_width = width // 2

    roi1 = img[:, :roi_width]
    roi2 = img[:, roi_width:2 * roi_width]
    roi3 = img[:, 2 * roi_width:]
    # 对每个ROI计算白色像素比例,判断该ROI是否包含目标
    threshold = 0.0001

    white_pixels2 = np.sum(roi2 > 250) / (roi_width * height)
    has_obj2 = white_pixels2 > threshold

    sum_profile2 = []
    if not has_obj2:
        for row in roi2:
            sum_profile2.append(0)
    if has_obj2:
        for row in roi2:
            sum_profile2.append(round(np.sum(row), 2))

    sum_profiles.append(np.asarray(sum_profile2))

df = pd.DataFrame(sum_profiles)
df.to_excel('sum_profiles.xlsx', index=False)
from sklearn.svm import SVC

data = pd.read_excel('sum_profiles.xlsx', header=0)

# 提取训练集X，去除最后一列
X = np.array(data.iloc[:, :-1])

# 提取标签y，最后一列
y = np.array(data.iloc[:, -1])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

# 创建并训练分类器
clf = SVC()
clf.fit(X_train, y_train)

# 在验证集上进行预测
y_pred = clf.predict(X_val)

# 计算精度评分
accuracy = accuracy_score(y_val, y_pred)
# 保存模型到文件
with open('model.pkl', 'wb') as file:
    pickle.dump(clf, file)
print("Accuracy:", accuracy)
