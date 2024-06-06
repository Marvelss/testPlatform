"""
@Author : SakuraFox
@Time: 2024-06-06 10:12
@File : cellular_automataV2.py
@Description : 元胞自动机可视化版本2
注意：
1.图像生成路径与excel文件一致
2.确保最终文件名称格式为任意名称+_+DayOfYear,如S/E/Y_156
3.输入Excel表格(E/Y结果,S则输入其他任意值)第一个单元格数值,以便于标识色带显示
"""

import gc
import math
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from PIL import Image


# 获取图像标题信息:S/E和Day Of Year
def getImageTitle(excelFileName):
    fileName = excelFileName.split('.')[0]
    # 按照最后一个下划线分割字符串
    temp = fileName.rsplit('_', 1)
    subtitle, doy = temp[0], temp[1]
    return fileName, subtitle, doy


# 生成热力图
def getImage(dataFilePath: str, outputDir: str, min_row: int, max_row: int, min_col: int, max_col: int,
             ribbonFlagNum: int) -> None:
    """
    :param min_col:
    :param max_col:
    :param min_row:
    :param max_row:
    :param outputDir: 输出图片路径
    :param dataFilePath: 读取excel文件
    :param ribbonFlagNum: 表格第一行第一个数值,区分色带
    """
    # with tqdm(total=len(os.listdir(dataDirPath))) as pbar:
    # for data_path in os.listdir(dataDirPath):
    #     if data_path.endswith('.xls'):
    last_part_basename = os.path.basename(dataFilePath)
    fileName, subtitle, doy = getImageTitle(last_part_basename)
    sideLength, use_min_row, use_max_row, use_col_list = rangeSetting(min_row, max_row, min_col, max_col)
    df = pd.read_excel(
        dataFilePath,
        header=None,
        skiprows=int(use_min_row),
        nrows=int(use_max_row - use_min_row),
        usecols=use_col_list)
    f, ax = plt.subplots(1, 1)
    ribbonFlag = df.iloc[0, 0]

    if ribbonFlag == ribbonFlagNum:
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

    ax.set_title('Day Of Years:{} SubTitle:{}'.format(doy, subtitle))
    f.savefig(os.path.join(outputDir, fileName + '.png'), dpi=500, bbox_inches='tight')
    # print(f'生成图像{dataFilePath}')
    # pbar.update(1)


# 自定义表格范围
def rangeSetting(min_row, max_row, min_col, max_col):
    use_col_list = []
    sideLength = max_col - min_col - max_row + min_row
    use_min_row, use_max_row = min_row - sideLength / 2, max_row + sideLength / 2
    for num in range(min_col, max_col + 1):
        use_col_list.append(num)
    return sideLength, use_min_row, use_max_row, use_col_list


# 转换成gif
def getGif(imageDirPath, gifDirPath):
    # 图片文件名列表
    images = []
    with tqdm(total=len(os.listdir(imageDirPath)) // 2) as pbar:
        for data_path in os.listdir(imageDirPath):
            if data_path.endswith('.png'):
                # 打开图片
                images.append(Image.open(os.path.join(imageDirPath, data_path)))

                # 设置输出 GIF 文件名
                output_gif = gifDirPath + '.gif'

                # 将图片保存为 GIF
                images[0].save(
                    output_gif,
                    save_all=True,
                    append_images=images[1:],
                    duration=1000,  # 设置每张图片的显示时间（毫秒）
                    loop=0,  # 设置循环次数，0 表示不循环
                )
                pbar.update(1)


def getImagesCount(dataDirRootT):
    # 计算总文件个数
    countGIFT = 0
    for rootT, dirsT, filesT in os.walk(dataDirRootT):
        if len(filesT) != 0 and filesT[0].endswith('.xls'):
            countGIFT += 1
    return countGIFT


def start(dataDirRoot, min_row, max_row, min_col, max_col, ExcelFirstElementNum, ImagesCount):
    # 深度遍历
    countGIF = 0
    for root, dirs, files in os.walk(dataDirRoot):
        if len(files) != 0 and files[0].endswith('.xls'):
            gifDirPath1 = os.path.join(root, 'gif_' + files[0].split('.')[0])
            countGIF += 1
            count = 0
            print(f'-----------------进度:{countGIF}/{ImagesCount}-----------------')
            print(f'当前计算路径:{root}')
            # print(f'Excel内容:{files}')
            print('开始生成Img图像')
            with tqdm(total=len(files)) as pbar1:
                for file in files:
                    dfFilePath = os.path.join(root, file)
                    try:
                        getImage(dfFilePath, root, min_row, max_row, min_col, max_col, ExcelFirstElementNum)
                        count += 1
                        # print('热力图像生成完成')
                    except Exception as e:
                        print(f"Error processing image{e}")
                    finally:
                        # 手动调用垃圾回收
                        gc.collect()
                    pbar1.update(1)
                print(f'开始合成GIF图像:{gifDirPath1}')
                getGif(root, gifDirPath1)


if __name__ == '__main__':
    # 表格范围
    min_rowM, max_rowM, min_colM, max_colM = 38, 60, 71, 100
    # 提示用户输入面状数据文件夹名称
    dataDirName = input('请输入面状数据文件夹名称: ')
    # 初始化标记值
    ExcelFirstElementNumM = int(input('输入Excel表格第一个单元格数值,以便于标识色带显示: '))
    dataDirRootM = os.path.join(os.getcwd(), dataDirName)
    # 计算总数量
    ImagesCountM = getImagesCount(dataDirRootM)
    print(f'最终输出GIF文件数量:{str(ImagesCountM)}')
    startFlag = input('输入start启动程序')
    if startFlag == 'start':
        # 启动程序
        start(dataDirRootM, min_rowM, max_rowM, min_colM, max_colM, ExcelFirstElementNumM, ImagesCountM)

