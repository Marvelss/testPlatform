"""
@Author : SakuraFox
@Time: 2024-11-26 8:59
@File : demo155.py
@Description : PYQT-根据URL下载文件
1.多线程编程方式
2.自动从URL下载文件的同时，可以更新UI界面进度条和在文本框输入文字
"""
from PyQt5.QtWidgets import QMainWindow,  QApplication
import sys

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QProgressBar, QPushButton

import requests
from PyQt5.QtCore import QThread, pyqtSignal


class DownloadThread(QThread):
    progressSignal = pyqtSignal(int)  # 发送下载进度信号
    logSignal = pyqtSignal(str)  # 发送日志信息信号

    def __init__(self, url, parent=None):
        super(DownloadThread, self).__init__(parent)
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()  # 检查响应状态
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open('downloaded_file.zip', 'wb') as f:
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    downloaded += len(data)
                    progress = int((downloaded / total_size) * 100)
                    self.progressSignal.emit(progress)  # 发射进度信号
            self.logSignal.emit("下载完成！")  # 完成日志
        except Exception as e:
            self.logSignal.emit(f"下载失败: {str(e)}")


class UpdateDialog(QDialog):
    def __init__(self, url, parent=None):
        super(UpdateDialog, self).__init__(parent)
        self.setWindowTitle("更新下载中")

        self.layout = QVBoxLayout(self)

        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setText('测试多线程')
        self.log_text_edit.setReadOnly(False)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # 范围0到100

        self.layout.addWidget(self.log_text_edit)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

        # 开始下载的线程
        self.download_thread = (
            DownloadThread(url))
        self.download_thread.progressSignal.connect(self.update_progress)
        self.download_thread.logSignal.connect(self.update_log)

        # 启动下载线程
        self.download_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)  # 更新进度条

    def update_log(self, message):
        self.log_text_edit.append(message)  # 更新日志信息


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("主窗口")

        self.update_button = QPushButton("检查更新", self)
        self.update_button.clicked.connect(self.check_update)
        self.setCentralWidget(self.update_button)

    def check_update(self):
        url = "https://github.com/MCSLTeam/MCSL2/releases/download/v2.2.6.3/MCSL2-2.2.6.3-Windows-x64.zip"  # 你的文件URL
        update_dialog = UpdateDialog(url, self)
        update_dialog.exec_()  # 启动对话框


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
