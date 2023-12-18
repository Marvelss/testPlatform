# 元胞自动机-面状数据可视化
import math
import os
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from PIL import Image


# 生成热力图
def getImage(dataDirPath, outputDir):
    """
    :param outputDir: 输出图片路径
    :param dataDirPath: 读取excel文件夹路径
    :return:
    """
    group_flag = 0
    with tqdm(total=len(os.listdir(dataDirPath))) as pbar:
        for data_path in os.listdir(dataDirPath):
            name = data_path.split('.')[0]
            group_id = name[-int(len(name)):-4]  # 组号
            if group_flag != group_id and not os.path.exists(os.path.join(outputDir, group_id)):
                group_flag = group_id
                os.mkdir(os.path.join(outputDir, group_id))
            day_id = name[-4:-1]  # day of years
            # print(group_id, day_id)
            # time.sleep(10)
            sideLength, use_min_row, use_max_row, use_col_list = rangeSetting()
            df = pd.read_excel(
                os.path.join(dataDirPath, data_path),
                header=None,
                skiprows=int(use_min_row),
                nrows=int(use_max_row - use_min_row),
                usecols=use_col_list)
            f, ax = plt.subplots(1, 1)
            sns.heatmap(df, cmap='RdYlGn_r', linewidths=0.1,
                        vmin=0, vmax=1)

            # print('------------------------------------')
            # print('x轴刻度')
            y_label = []
            # 这里的设置可能导致x轴数值不精确
            num = math.ceil(use_min_row)
            for _ in range(len(ax.get_xticklabels())):
                y_label.append(num)
                num += 2
            # print(y_label)
            # 打印x轴标签
            # print()
            ax.set_yticklabels(y_label)

            # 设置Axes的标题
            ax.set_title('Group:{} Day Of Years:{}'.format(group_id, day_id))
            f.savefig(os.path.join(outputDir, group_id, name + '.png'), dpi=500, bbox_inches='tight')
            pbar.update(1)


# 自定义表格范围
def rangeSetting():
    min_row, max_row, min_col, max_col = 38, 60, 71, 100
    use_col_list = []
    sideLength = max_col - min_col - max_row + min_row
    use_min_row, use_max_row = min_row - sideLength / 2, max_row + sideLength / 2
    # print('间距上下扩展数值')
    # print(sideLength)
    # print('------------------------------------')
    # print('扩展后最大最小行')
    # print(use_min_row, use_max_row)
    for i in range(min_col, max_col + 1):
        use_col_list.append(i)
    # print('------------------------------------')
    # print('y轴列')
    # print(use_col_list)
    return sideLength, use_min_row, use_max_row, use_col_list


# 转换成gif
def getGif(imageDirPath, gifDirPath, groupId):
    # 图片文件名列表
    images = []
    with tqdm(total=len(os.listdir(imageDirPath))) as pbar:
        for data_path in os.listdir(imageDirPath):
            # 打开图片
            images.append(Image.open(os.path.join(imageDirPath, data_path)))

            # 设置输出 GIF 文件名
            output_gif = os.path.join(gifDirPath, 'y_output' + str(groupId) + '.gif')

            # 将图片保存为 GIF
            images[0].save(
                output_gif,
                save_all=True,
                append_images=images[1:],
                duration=1000,  # 设置每张图片的显示时间（毫秒）
                loop=0,  # 设置循环次数，0 表示不循环
            )
            pbar.update(1)


dataDirPathMain = 'ca_result_y'
gifDir = r'E:\a_python\program\testPlatform\surfacedatavisualization\images\gif_ca_result_y'
for i in range(1, 15):
    print(i)
    imageDir = os.path.join(r'E:\a_python\program\testPlatform\surfacedatavisualization\images\image_ca_result_y',
                            str(i))
    getGif(imageDir, gifDir, i)
# getImage(dataDirPathMain, imageDir)
