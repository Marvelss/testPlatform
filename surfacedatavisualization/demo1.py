import math
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from PIL import Image

"""
@Author  : SakuraFox
@Time    : 2023-12-20 10:10
@File    : demo.py
@Description : 面状数据可视化-以元胞自动机为例,
将结果输出在同级目录下的images中,包括原始热力图和合成后的GIF图

注意:
1.面状数据和py文件放在同一目录下
2.
"""


# 生成热力图
def getImage(dataDirPath: str, outputDir: str, min_row: int, max_row: int, min_col: int, max_col: int) -> None:
    """
    :param min_col:
    :param max_col:
    :param min_row:
    :param max_row:
    :param outputDir: 输出图片路径
    :param dataDirPath: 读取excel文件夹路径
    :return:
    """
    group_flag = 0
    with tqdm(total=len(os.listdir(dataDirPath))) as pbar:
        for data_path in os.listdir(dataDirPath):
            # 生成的文件名
            name = data_path.split('.')[0]
            # 参数名称
            parameter = data_path.split('.')[0][-1]
            group_id = name[-int(len(name)):-4]  # 组号
            if group_flag != group_id and not os.path.exists(os.path.join(outputDir, group_id)):
                group_flag = group_id
                os.mkdir(os.path.join(outputDir, group_id))
            day_id = name[-4:-1]  # day of years
            # print(group_id, day_id)
            # time.sleep(10)
            sideLength, use_min_row, use_max_row, use_col_list = rangeSetting(min_row, max_row, min_col, max_col)
            df = pd.read_excel(
                os.path.join(dataDirPath, data_path),
                header=None,
                skiprows=int(use_min_row),
                nrows=int(use_max_row - use_min_row),
                usecols=use_col_list)
            f, ax = plt.subplots(1, 1)
            ribbonFlag = df.iloc[0, 0]

            if not ribbonFlag:
                sns.heatmap(df, cmap='RdYlGn_r', linewidths=0.1,
                            vmin=0, vmax=1)
            else:
                sns.heatmap(df, cmap='RdYlGn', linewidths=0.1,
                            vmin=0, vmax=1)
            # 这里的设置可能导致x轴数值不精确
            # 根据x轴刻度获取Y轴标签数值
            y_label = []
            num = math.ceil(use_min_row)
            for _ in range(len(ax.get_xticklabels())):
                y_label.append(num)
                num += 2
            # 设置Y轴标签
            ax.set_yticklabels(y_label)
            # 设置Axes的标题
            ax.set_title('Parameter:{} Group:{} Day Of Years:{}'.format(parameter, group_id, day_id))
            f.savefig(os.path.join(outputDir, group_id, name + '.png'), dpi=500, bbox_inches='tight')
            pbar.update(1)


# 自定义表格范围
def rangeSetting(min_row, max_row, min_col, max_col):
    use_col_list = []
    sideLength = max_col - min_col - max_row + min_row
    use_min_row, use_max_row = min_row - sideLength / 2, max_row + sideLength / 2
    for num in range(min_col, max_col + 1):
        use_col_list.append(num)
    return sideLength, use_min_row, use_max_row, use_col_list


# 转换成gif
def getGif(imageDirPath, gifDirPath, groupId):
    # 图片文件名列表
    images = []
    with tqdm(total=len(os.listdir(imageDirPath))) as pbar:
        for data_path in os.listdir(imageDirPath):
            parameter = data_path.split('.')[0][-1]
            # 打开图片
            images.append(Image.open(os.path.join(imageDirPath, data_path)))

            # 设置输出 GIF 文件名
            output_gif = os.path.join(gifDirPath, parameter + '_output' + str(groupId) + '.gif')

            # 将图片保存为 GIF
            images[0].save(
                output_gif,
                save_all=True,
                append_images=images[1:],
                duration=1000,  # 设置每张图片的显示时间（毫秒）
                loop=0,  # 设置循环次数，0 表示不循环
            )
            pbar.update(1)


def start(dataDirNameList, min_row, max_row, min_col, max_col):
    for tempDataPath in dataDirNameList:
        # 主文件夹路径
        outputDirPath = os.path.join(ROOT_PATH, 'images')
        # 生成的热力图路径
        imageDirPath1 = os.path.join(ROOT_PATH, 'images', 'img_' + tempDataPath)
        # 合成后的gif热力图路径
        gifDirPath1 = os.path.join(ROOT_PATH, 'images', 'gif_' + tempDataPath)
        if not os.path.exists(outputDirPath):
            os.mkdir(outputDirPath)
        if not os.path.exists(imageDirPath1):
            # print(imageDirPath1)
            os.mkdir(imageDirPath1)
        if not os.path.exists(gifDirPath1):
            os.mkdir(gifDirPath1)
            # print(gifDirPath1)
        dataPath = os.path.join(ROOT_PATH, tempDataPath)

        print('文件夹:{} 开始生成热力图'.format(tempDataPath))
        getImage(dataPath, imageDirPath1, min_row, max_row, min_col, max_col)
        print('热力图像生成完成')

        # 合成GIF,不需要该功能可注释以下内容
        # 循环次数为组数,后续可扩展成自动获取组数
        print('开始合成GIF')
        for i in range(1, 15):
            tempImageDir = os.path.join(imageDirPath1, str(i))
            getGif(tempImageDir, gifDirPath1, i)
            print('第{}组完成'.format(str(i)))


if __name__ == '__main__':
    print('***********************初始化参数设置***********************')
    # 表格范围
    min_row1, max_row1, min_col1, max_col1 = 38, 60, 71, 100
    # 面状数据文件夹名称
    dataDirNameTempList = ['ca_result_e', 'ca_result_s', 'ca_result_y']

    ROOT_PATH = os.getcwd()

    # 程序运行
    start(dataDirNameTempList, min_row1, max_row1, min_col1, max_col1)
