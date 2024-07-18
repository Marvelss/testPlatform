"""
@Author : SakuraFox
@Time: 2024-07-18 17:35
@File : demo142.py
@Description : 调整PDF页面尺寸
"""
import fitz, os, img2pdf

file_path = '2024-杭电-神农英才-佐证-盖章-2.pdf'  # PDF 文件路径
src = fitz.open(file_path)
doc = fitz.open()  # new output PDF
for page in src:
    w, h = page.rect.br  # extract input page widht and height
    print(w)
    print(h)
    newpage = doc.new_page(width=1.2*w, height=1.202*h)
    newpage.show_pdf_page(newpage.rect, src, page.number)
doc.ez_save("2024-杭电-神农英才-佐证-盖章-2-调整尺寸.pdf")