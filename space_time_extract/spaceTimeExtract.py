"""
@Author : SakuraFox
@Time: 2024-05-16 20:08
@File : spaceTimeExtract.py
@Description : 时空抽取
1.基于活动积温的生育期计算
2.基于不同生育期的时空特征抽取
"""
import glob
import os
import time

from osgeo import gdal
from tqdm import trange
import numpy as np
import rasterio


def accumulate_values(arr, target_sum):
    print('获取起点日期中...')
    x_dim, y_dim, z_dim = arr.shape
    # 输出day of year起始数组
    result = np.zeros((x_dim, y_dim), dtype=arr.dtype)
    # result = np.full((x_dim, y_dim), np.nan, dtype=arr.dtype)
    # 按照z轴对每个像素点累加
    cumulative_sum = np.cumsum(arr, axis=2)
    # 找到第一个大于150的z轴值,也就是初始温度
    for i in trange(cumulative_sum.shape[0]):
        for j in range(cumulative_sum.shape[1]):
            # if i == 909 and j == 116:
            #     print(cumulative_sum[i, j])
            # time.sleep(20)
            idx = np.argmax(cumulative_sum[i, j] >= target_sum)
            if idx != 0:
                result[i, j] = idx + 1
    # result = np.where(result == 0, -9999, result)
    return result


def space_time_extract(template_tif_path, temperature_dir, cumulated_temperature, durationTemp):
    """
    :param template_tif_path: 模板tif文件路径,主要用于获取tif图像属性
    :param temperature_dir: 包含全部气象或遥感等数据的文件夹路径
    :param cumulated_temperature: 达到病害敏感时段起点的活动积温
    :param durationTemp: 抽取天数
    :return: result: 输出结果,二维数据
    """
    template_data = rasterio.open(template_tif_path)
    rows = template_data.width
    cols = template_data.height
    template_list = np.transpose(template_data.read(1))
    template_data.close()
    # 获取该文件夹下所有tif文件(得按照一年中的第几天的大小一次排序)
    tif_files = glob.glob(temperature_dir + '/*.tif')
    # z轴为现存数据天数，通过文件个数确定
    days_max = len(tif_files)
    # 汇聚全部气象数据数组
    temperature = np.zeros((rows, cols, days_max), dtype=np.float32)
    x, y = template_list.shape
    # 输出图层
    result = np.zeros((rows, cols), dtype=np.float32)
    print('获取全部气象数据中...')
    # time.sleep(1)
    # 获取366天气象数据
    for z in trange(days_max):
        file = tif_files[z]
        dataset = rasterio.open(file)
        pixel_value = dataset.read(1)
        # 对pixel_value进行转置
        pixel_value = np.transpose(pixel_value)
        # 读取像素的数据,将二维矩阵赋值给三维矩阵中的每个z维度
        temperature[:, :, z] = pixel_value
        dataset.close()
    # 获取起点日期
    doy_list = accumulate_values(temperature, cumulated_temperature)

    # 转置结果
    doy_list_result = np.transpose(doy_list)
    print('生成DOY图像')
    generate_tif(doy_list_result, template_tif_path1, saved_path2)

    print(doy_list[116, 909])
    print(doy_list[216, 909])
    print(doy_list[316, 909])
    print(doy_list[416, 909])
    print(doy_list[516, 909])
    print('获取输出tif图数据中...')
    # time.sleep(1)
    # 遍历每个像素
    for i in trange(x):
        for j in range(y):
            # 累积温度
            accumulate_temperature = 0
            # 空值跳过
            if doy_list[i, j] == 0:
                continue
            for offset in range(durationTemp):
                # 累积温度
                # 该方式可能也可以使用
                # cumulative_sum = np.cumsum(arr, axis=2)
                accumulate_temperature = accumulate_temperature + temperature[i, j, int(doy_list[i, j]) + offset]
            # 输出总累积温度
            result[i, j] = accumulate_temperature
            # 输出总平均温度
            # result[i, j] = accumulate_temperature / durationTemp
    transpose_result = np.transpose(result)
    return transpose_result


def generate_tif(result_array, template_tif_path, saved_path):
    """

    :param result_array: 输出像素数据,二维数据
    :param template_tif_path: 模板tif文件路径,主要用于获取tif图像属性
    :param saved_path: 保存tif文件路径
    :return:
    """
    # 打开已有tif文件
    with rasterio.open(template_tif_path) as src:
        # 获取空间参考系统
        crs_template = src.crs
        # 获取转换矩阵
        transform_template = src.transform
        # 获取二维数组的形状和数据类型：
        height, width = result_array.shape
        data_type = result_array.dtype
    # 定义空间参考系统和转换矩阵：
    crs = crs_template  # 使用模板空间参考系统
    transform = transform_template  # 使用模板转换矩阵
    # 创建输出文件并写入数据：
    with rasterio.open(saved_path, 'w', driver='GTiff', height=height, width=width, count=1, dtype=data_type,
                       crs=crs,
                       transform=transform,
                       nodata=0) as dst:
        dst.write(result_array, 1)
    print('保存成功,路径为:{}'.format(os.path.join(os.getcwd(), saved_path)))


template_tif_path1 = r'tif_250m\T20200101.tif'
saved_path1 = 'SpatiotemporalExtractionResult.tif'
saved_path2 = 'DayOfYear-ActiveAccumulatedTemperature.tif'
temperature_dir1 = 'tif_250m'
duration = 10
active_accumulated_temperature = 150
result1 = space_time_extract(template_tif_path1, temperature_dir1, active_accumulated_temperature, duration)
generate_tif(result1, template_tif_path1, saved_path1)

print('==================verify==================')
path2 = saved_path1
doy_data2 = rasterio.open(path2)
print(doy_data2.read(1)[116, 909])
print(doy_data2.read(1)[216, 909])
print(doy_data2.read(1)[316, 909])
print(doy_data2.read(1)[416, 909])
print(doy_data2.read(1)[516, 909])
