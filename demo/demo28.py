"""
@Author  : SakuraFox
@Time    : 2023-12-25 9:21
@File    : demo28.py
@Description : 马铃薯分类
"""
import cv2
import numpy as np

import os

potato_dir = 'potatoes'
stone_dir = 'stones'

sum_profiles = []

labels = []
for img_path in os.listdir(potato_dir):
    img = cv2.imread(os.path.join(potato_dir, img_path))
    # 处理土豆图片
    labels.append(0)  # 0表示土豆

for img_path in os.listdir(stone_dir):
    img = cv2.imread(os.path.join(stone_dir, img_path))
    # 处理石头图片
    labels.append(1)  # 1表示石头

# 设置3个ROI区域,将图像划分为3个通道,每个通道可能包含土豆、石块或为空

for img_path in os.listdir(potato_dir):
    img = cv2.imread(os.path.join(potato_dir, img_path))
    height, width = img.shape[:2]
    roi_width = width // 2

    roi1 = img[:, :roi_width]
    roi2 = img[:, roi_width:2 * roi_width]
    roi3 = img[:, 2 * roi_width:]
    # 对每个ROI计算白色像素比例,判断该ROI是否包含目标
    threshold = 0.0001

    white_pixels1 = np.sum(roi1 > 250) / (roi_width * height)
    has_obj1 = white_pixels1 > threshold

    white_pixels2 = np.sum(roi2 > 250) / (roi_width * height)
    has_obj2 = white_pixels2 > threshold

    white_pixels3 = np.sum(roi3 > 250) / (roi_width * height)
    has_obj3 = white_pixels3 > threshold
    print(white_pixels1, white_pixels2, white_pixels3)
    # 如果ROI包含目标,计算每个行的像素和,得到散射曲线
    sum_profile1 = []
    if has_obj1:
        for row in roi1:
            sum_profile1.append(np.sum(row))
    else:
        sum_profile1.append(np.sum([0] * height))
    sum_profile2 = []
    if has_obj2:
        for row in roi2:
            sum_profile2.append(np.sum(row))
    else:
        sum_profile2.append(np.sum([0] * height))
    sum_profile3 = []
    if has_obj3:
        for row in roi3:
            sum_profile3.append(np.sum(row))
    else:
        sum_profile3.append(np.sum([0] * height))
    # print(sum_profile1, sum_profile2, sum_profile3)
    sum_profiles.append(sum_profile1)
    sum_profiles.append(sum_profile2)
    sum_profiles.append(sum_profile3)

for img_path in os.listdir(stone_dir):
    img = cv2.imread(os.path.join(stone_dir, img_path))
    height, width = img.shape[:2]
    roi_width = width // 2

    roi1 = img[:, :roi_width]
    roi2 = img[:, roi_width:2 * roi_width]
    roi3 = img[:, 2 * roi_width:]
    # 对每个ROI计算白色像素比例,判断该ROI是否包含目标
    threshold = 0.0001

    white_pixels1 = np.sum(roi1 > 250) / (roi_width * height)
    has_obj1 = white_pixels1 > threshold

    white_pixels2 = np.sum(roi2 > 250) / (roi_width * height)
    has_obj2 = white_pixels2 > threshold

    white_pixels3 = np.sum(roi3 > 250) / (roi_width * height)
    has_obj3 = white_pixels3 > threshold
    # 如果ROI包含目标,计算每个行的像素和,得到散射曲线
    sum_profile1 = []
    if has_obj1:
        for row in roi1:
            sum_profile1.append(np.sum(row))
    else:
        sum_profile1.append(np.sum([0] * height))
    sum_profile2 = []
    if has_obj2:
        for row in roi2:
            sum_profile2.append(np.sum(row))
    else:
        sum_profile2.append(np.sum([0] * height))
    sum_profile3 = []
    if has_obj3:
        for row in roi3:
            sum_profile3.append(np.sum(row))
    else:
        sum_profile3.append(np.sum([0] * height))

    sum_profiles.append(sum_profile1)
    sum_profiles.append(sum_profile2)
    sum_profiles.append(sum_profile3)

from sklearn.svm import SVC

X = np.array(sum_profiles)
y = np.array(labels)

# print(sum_profiles)
# print(X.shape)
# print(y.shape)
clf = SVC()
clf.fit(X, y)
