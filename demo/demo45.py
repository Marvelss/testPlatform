"""
@Author  : SakuraFox
@Time    : 2024-02-12 1:01
@File    : demo45.py
@Description : 读取并修改pdf内容(插入文字和图片)
"""
import fitz  # PyMuPDF


def insertText(locationX, locationY, content):
    # 使用内置的“Droid Sans Fallback Regular”字体添加中文文本
    addressLocation = fitz.Point(locationX, locationY)  # 示例位置，请根据需要调整
    # 在添加文本时不需要显式指定字体
    page.insert_text(addressLocation, content,
                     fontname="HT", fontfile=r"msyh.ttc", fontsize=11)  # 添加文本


def insertImage(locationSX, locationSY, locationEX, locationEY, imagePath):
    # 替换图片
    imageLocation = fitz.Rect(locationSX, locationSY, locationEX, locationEY)  # 示例图片位置，请根据需要调整
    page.insert_image(imageLocation, filename=imagePath)  # 插入图片


# 打开原始PDF文件
pdf_path = 'template.pdf'  # 请替换为你的PDF文件路径
# 保存修改后的PDF文件
new_pdf_path = 'modified_pdf.pdf'  # 修改后的PDF文件保存路径
doc = fitz.open(pdf_path)
# 选择第一页（或者是包含表格的特定页面）
page = doc[0]

# =============================公司信息=============================

addressContent = ''
companyContent = ""
personPhoneContent = ""  # 中文内容
countContent = ""
insertText(65, 130, addressContent)
insertText(65, 165, companyContent)
insertText(65, 180, personPhoneContent)
insertText(365, 243, countContent)

# =============================注册号=============================
RegisterContent = "15633616"  # 中文内容
insertText(50, 247, RegisterContent)

# =============================商标=============================
insertImage(140, 240, 210, 310, r'0.png')
insertImage(210, 240, 280, 310, r'1.png')
insertImage(140, 310, 210, 380, r'2.png')
insertImage(210, 310, 280, 380, r'3.png')

doc.save(new_pdf_path)

# 关闭文档
doc.close()
