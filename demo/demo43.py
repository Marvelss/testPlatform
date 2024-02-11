"""
@Author  : SakuraFox
@Time    : 2024-02-11 21:22
@File    : demo43.py
@Description : pdf打印
将多个pdf合并为一个文件后，调用PDFtoPrinter.exe打印
"""

import time
import subprocess
import sys
import os
import win32com.client as win32
import win32com.client
from glob import glob

import win32print
from pikepdf import Pdf

pdf = Pdf.new()
path = r'E:\a_python\program\testPlatform\noticefile2\*.pdf'
for file in glob(path):
    src = Pdf.open(file)
    pdf.pages.extend(src.pages)

pdf.save('merged.pdf')


def start_printer(cprinter, pdf):
    if sys.platform == 'win32':
        args = [f"{os.path.dirname(__file__)}\PDFtoPrinter.exe",
                f"{pdf}",
                f"{cprinter}",
                ]
        subprocess.run(args, encoding="utf-8", shell=True)
    print(f"\t|已发送至打印机：{cprinter}")


s = time.perf_counter()
start_printer(win32print.GetDefaultPrinter(), 'merged.pdf')
elapsed = time.perf_counter() - s
print(f"第三方打印 executed in {elapsed:0.2f} seconds.")
