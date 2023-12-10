import os
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from PIL import Image


def get_gif(image_dir_path, gif_dir_path):
    # 图片文件名列表

    image_files = [os.path.join(image_dir_path, filename) for filename in os.listdir(image_dir_path)]
    # print(image_files)
    # 打开图片
    images = [Image.open(filename) for filename in image_files]

    # 设置输出 GIF 文件名
    output_gif = os.path.join(gif_dir_path, 'output1.gif')

    # 将图片保存为 GIF
    images[0].save(
        output_gif,
        quality=100,
        save_all=True,
        append_images=images[1:],
        duration=2000,  # 设置每张图片的显示时间（毫秒）
        loop=0,  # 设置循环次数，0 表示不循环
    )


image_path = r'E:\a_python\program\testPlatform\demo\image\image_e\10'
gif_path = r'E:\a_python\program\testPlatform\demo\image\gif_e'
get_gif(image_path, gif_path)
