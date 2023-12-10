import os
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from PIL import Image


# 生成热力图
def get_image(data_dir_path, output_dir):
    """

    :param data_dir_path: 读取excel文件夹路径
    :param output_dir: 输出图片路径
    :return:
    """
    group_flag = 0
    with tqdm(total=len(os.listdir(data_dir_path_main))) as pbar:
        for data_path in os.listdir(data_dir_path):
            name = data_path.split('.')[0]
            group_id = name[-int(len(name)):-4]  # 组号
            if group_flag != group_id and not os.path.exists(os.path.join(output_dir, group_id)):
                group_flag = group_id
                os.mkdir(os.path.join(output_dir, group_id))
            day_id = name[-4:-1]  # day of years
            # print(group_id, day_id)
            time.sleep(10)
            df = pd.read_excel(
                os.path.join(data_dir_path, data_path), header=None)
            f, ax = plt.subplots(1, 1)
            sns.heatmap(df, cmap='RdYlGn_r', linewidths=0.1,
                        vmin=0, vmax=1)
            # 设置Axes的标题
            ax.set_title('Group:{} Day Of Years:{}'.format(group_id, day_id))
            f.savefig(os.path.join(output_dir, group_id, name + '.png'), dpi=500, bbox_inches='tight')
            pbar.update(1)


# 转换成gif
def get_gif(image_dir_path, gif_dir_path):
    # 图片文件名列表

    images = []
    with tqdm(total=len(os.listdir(data_dir_path_main))) as pbar:
        for data_path in os.listdir(image_dir_path):
            # 打开图片
            images.append(Image.open(os.path.join(image_dir_path, data_path)))

            # 设置输出 GIF 文件名
            output_gif = os.path.join(gif_dir_path, 'output.gif')

            # 将图片保存为 GIF
            images[0].save(
                output_gif,
                save_all=True,
                append_images=images[1:],
                duration=2000,  # 设置每张图片的显示时间（毫秒）
                loop=0,  # 设置循环次数，0 表示不循环
            )
            pbar.update(1)


data_dir_path_main = r'E:\a_python\program\testPlatform\demo\ca_result_e'
image_dir = r'E:\a_python\program\testPlatform\demo\image\image_e'
get_image(data_dir_path_main, image_dir)
# print(len(os.listdir(data_dir_path_main)))
