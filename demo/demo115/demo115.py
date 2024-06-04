"""
@Author : SakuraFox
@Time: 2024-06-04 9:33
@File : demo115.py
@Description : 基于栅格数据的excel转化GeoJson数据
测试数据:
1.day of year数据
2.基于day of year累积10天温度
"""

import pandas as pd
import json


def excelToJson(inputFilePath, outputFilePath, idField, lonField, latField, valueField, ):
    """

    :param inputFilePath: 输入excel表格文件路径
    :param outputFilePath: 输出Json文件路径
    :param idField: 标记,可使用表格内唯一值字段名称
    :param lonField: 表格内经度字段名称
    :param latField: 表格内纬度字段名称
    :param valueField: 表格像元值字段名称
    :return: Json文件
    """
    df = pd.read_excel(inputFilePath)

    # Correctly parsed dataframe:
    #    GRID_CODE        lat         lon
    # 0         68  31.163856  119.668872
    # 1         68  31.163856  119.719872
    # 2         68  31.163856  119.736872

    # GeoJSON template
    geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "id": "ak16994521",
                    "mag": 2.3,
                    "time": 1507425650893,
                    "felt": None,
                    "tsunami": 0
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -151.5129,
                        63.1016,
                        0
                    ]
                }
            }
        ]
    }

    # Adding new features from the dataframe
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "properties": {
                "id": row[idField],
                "mag": row[valueField],  # Assuming no magnitude data in the provided table
                "time": None,  # Assuming no time data in the provided table
                "felt": None,
                "tsunami": 0
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    row[lonField],
                    row[latField],
                    row[valueField]
                ]
            }
        }
        geojson['features'].append(feature)

    # Save to a GeoJSON file
    output_file = outputFilePath
    with open(output_file, 'w') as f:
        json.dump(geojson, f)


excelToJson('rastert_dayofya1_TableToExcel.xls',
            'test.json',
            'FID', 'lon',
            'lat', 'GRID_CODE')
