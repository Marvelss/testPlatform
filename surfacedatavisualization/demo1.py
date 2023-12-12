# 元胞自动机-面状数据可视化
import os
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from PIL import Image


# 生成热力图
def getImage(dataDirPath, outputDir, fillValue):
    """
    :param fillValue: 填充值,对excel面状数据进行填充,使其行与列等长
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
            df = pd.read_excel(
                os.path.join(dataDirPath, data_path), header=None)
            # 获取最大行或列,补全表格成方阵,使得热力图中的方格为正方形
            max_columns = max(df.shape[1], df.shape[0])
            df_filled = df.reindex(range(max_columns))
            df_filled = df_filled.fillna(fillValue)
            f, ax = plt.subplots(1, 1)
            sns.heatmap(df_filled, cmap='RdYlGn_r', linewidths=0.1,
                        vmin=0, vmax=1)
            # 设置Axes的标题
            ax.set_title('Group:{} Day Of Years:{}'.format(group_id, day_id))
            f.savefig(os.path.join(outputDir, group_id, name + '.png'), dpi=500, bbox_inches='tight')
            pbar.update(1)


# 转换成gif
def getGif(imageDirPath, gifDirPath):
    # 图片文件名列表
    images = []
    with tqdm(total=len(os.listdir(imageDirPath))) as pbar:
        for data_path in os.listdir(imageDirPath):
            # 打开图片
            images.append(Image.open(os.path.join(imageDirPath, data_path)))

            # 设置输出 GIF 文件名
            output_gif = os.path.join(gifDirPath, 'output.gif')

            # 将图片保存为 GIF
            images[0].save(
                output_gif,
                save_all=True,
                append_images=images[1:],
                duration=1000,  # 设置每张图片的显示时间（毫秒）
                loop=0,  # 设置循环次数，0 表示不循环
            )
            pbar.update(1)


dataDirPathMain = 'ca_result_e'
imageDir = 'images'
# getGif(dataDirPathMain, imageDir)
getImage(dataDirPathMain, imageDir, 0)
