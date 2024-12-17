"""
@Author : SakuraFox
@Time: 2024-12-02 16:16
@File : main.py
@Description : 面向网格数据的气象因子提取
1.利用rasterio将ASCII转换栅格
2.根据经纬度提取对应格点数据
"""

import os
import pandas as pd
from osgeo import gdal
import numpy as np
import rasterio
from rasterio.transform import from_origin


def ascToRaster(ascii_file, output_raster):
    """
    地理变换参数:EPSG:4326
    """
    # 读取 ASCII 数据
    with open(ascii_file, 'r') as file:
        lines = file.readlines()

    # 提取头信息
    ncols = int(lines[0].split()[1])
    nrows = int(lines[1].split()[1])
    xllcorner = float(lines[2].split()[1])
    yllcorner = float(lines[3].split()[1])
    cellsize = float(lines[4].split()[1])
    nodata_value = float(lines[5].split()[1])

    # 创建 numpy 数组
    data = np.loadtxt(lines[6:], dtype=float)

    # 创建 transform 参数
    transform = from_origin(xllcorner, yllcorner + nrows * cellsize, cellsize, cellsize)

    # 使用 rasterio 写入栅格
    with rasterio.open(
            output_raster,
            'w',
            driver='GTiff',
            height=nrows,
            width=ncols,
            count=1,
            dtype=data.dtype,
            crs='EPSG:4326',
            transform=transform,
            nodata=nodata_value,
    ) as dst:
        dst.write(data, 1)


# ASCII 数据文件路径
# ascii_fileT = 'raster_data2.txt'

# 读取ASCII文件对其进行转化
def convertASCIIFile(fileDir, rasterFileDirT):
    path = fileDir
    print(path)
    for root, dirs, files in os.walk(path):
        count = 1
        # 输出栅格文件路径# 打开ASCII文件

        for file in files:
            fileT2 = file.split('.')[1].split('-')[1]

            if 'MEAN' != fileT2:
                continue
            fileT1 = file.split('.')[1].split('-')[2]
            if '(' in fileT1:
                continue

            date = pd.to_datetime(fileT1, format='%Y%m%d')
            file_path = os.path.join(root, file)
            output_rasterT = os.path.join(
                os.getcwd(), rasterFileDirT, f'栅格_{date.year}_{date.dayofyear}.tif')
            count += 1
            if date.dayofyear == 366:
                continue
            ascToRaster(file_path, output_rasterT)
            print(output_rasterT)


def extract_info(filename):
    # 去掉文件扩展名
    base_name = os.path.basename(filename.split('.')[0])
    temp = base_name.split('_')
    # 根据'_'分割
    temperature_type = temp[0]
    year = temp[1]
    day_of_year = temp[2]
    return temperature_type, year, day_of_year, filename


def onSpatialPointExtract(lonLatFileT, rasterFileDirT, savedFileDirT):
    # 注册所有的gdal驱动
    gdal.AllRegister()
    df1 = pd.read_excel(lonLatFileT)
    path1 = rasterFileDirT
    count = 1

    # 打开数据集，处理每个文件
    for root, dirs, files in os.walk(path1):
        for file in files:
            file_path = os.path.join(root, file)
            f, year, day_of_year, _ = extract_info(file)
            featureFiledName = file.split('.')[0].split('_')[0]
            # 打开tif文件
            dataset = gdal.Open(file_path)
            # 获取地理变换参数
            adfGeoTransform = dataset.GetGeoTransform()

            # 获取栅格的列数和行数
            nXSize = dataset.RasterXSize  # 列数
            nYSize = dataset.RasterYSize  # 行数

            # 获取第一个波段
            band = dataset.GetRasterBand(1)
            data = band.ReadAsArray()
            # 保存结果
            results = []

            # 对 df1 中每个点，通过整数除法找到其所在的栅格位置
            for index, row in df1.iterrows():
                lon, lat = row['经度'], row['纬度']

                # 计算给定经纬度在栅格中的位置
                # 这里假设网格的经纬度间隔是已知的，例如1度经度和1度纬度
                lon_index = int((lon - adfGeoTransform[0]) / adfGeoTransform[1])
                lat_index = int((lat - adfGeoTransform[3]) / adfGeoTransform[5])

                # 确保索引不超出范围
                lon_index = min(max(lon_index, 0), nXSize - 1)
                lat_index = min(max(lat_index, 0), nYSize - 1)

                # 获取栅格值
                value = data[lat_index, lon_index]
                results.append(value)

            # 添加新列到df1
            df1['年'] = int(year)
            df1['DayOfYear'] = int(day_of_year)
            df1[featureFiledName] = results

            # 保存到 Excel
            df1.to_excel(os.path.join(savedFileDirT, f'result{count}.xlsx'), index=False)
            count += 1
            print(f'{file}完成')


def mergeExcel(excelFileDirT, extractFileT):
    # List to hold the DataFrames
    df_list = []

    # Traverse the folder to find all Excel files
    for filename in os.listdir(excelFileDirT):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            file_path = os.path.join(excelFileDirT, filename)

            # Read each Excel file into a DataFrame
            df = pd.read_excel(file_path)

            # Append the DataFrame to the list
            df_list.append(df)

    # Merge all the DataFrames on '经度', '纬度', and '年'
    merged_df = pd.DataFrame()

    if df_list:
        # Start by merging the first DataFrame in the list
        merged_df = df_list[0]

        # Iterate through the rest of the DataFrames and merge
        for df in df_list[1:]:
            # Merge the DataFrames on ['经度', '纬度', '年', 'DayOfYear']
            merged_df = pd.concat([merged_df, df], ignore_index=True)

            # Optionally, sort by ['经度', '纬度', '年', 'DayOfYear'] if needed
            merged_df = merged_df.sort_values(by=['经度', '纬度', '年', 'DayOfYear']).reset_index(drop=True)

    # Save the merged DataFrame to a new Excel file (optional)
    merged_df.to_excel(extractFileT, index=False)

    print(merged_df)


def makeDir(rasterFileDirT, excelFileDirT):
    if not os.path.exists(rasterFileDirT):
        os.makedirs(rasterFileDirT)
    if not os.path.exists(excelFileDirT):
        os.makedirs(excelFileDirT)


acsiiFileDir = r'F:\A_postgraduate\病虫害多场景系统\1a_师兄师姐文献及资料\论文相关数据\格网气象数据-原始数据\2000-2019年中国格网气象数据\气温'
rasterFileDir = os.path.join(os.getcwd(), 'rasterFile')
lonLatFile = '地区3.xlsx'
excelFileDir = os.path.join(os.getcwd(), 'excelFile')
extractFile = os.path.join(os.getcwd(), 'result.xlsx')

# 创建文件夹
makeDir(rasterFileDir, excelFileDir)
# 读取并转换ASCII文件为栅格
try:
    convertASCIIFile(acsiiFileDir, rasterFileDir)
except BaseException as e:
    print(e)
# 根据经纬度提取对应栅格值
onSpatialPointExtract(lonLatFile, rasterFileDir, excelFileDir)
# 合并所有excel文件为一个
mergeExcel(excelFileDir, extractFile)
