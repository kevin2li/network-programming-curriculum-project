import traceback
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import sys
from qt.qt_client import Ui_MainWindow
import requests
import json
import re
import threading


class Chatbot_Window(QMainWindow, Ui_MainWindow):
    def __init__(self, name):
        super(Chatbot_Window, self).__init__()
        self.setupUi(self)
        self.name = name
        self.base_url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={}"
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"}
        self.lineEdit.setFocus()
        self.listWidget_2.addItem(self.name + "<You>")
        self.setWindowIcon(QIcon('images/chatroom_icon.jpg'))
        self.show()

    def send(self):
        try:
            message = self.lineEdit.text()
            self.lineEdit.clear()
            self.lineEdit.setFocus()
            # add Item
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight)
            font = QtGui.QFont()
            font.setPointSize(12)
            item.setFont(font)
            item.setText(message+" <You>")
            self.listWidget.addItem(item)
            self.listWidget.scrollToBottom()
            threading.Thread(target=self.receive, args=(message, )).start()
        except:
            traceback.print_exc()

    def receive(self, message):
        url = self.base_url.format(message)
        r = requests.get(url, headers=self.headers)
        result = json.loads(r.text)
        result = re.sub("\{br\}", "\n", result['content'])
        # add Item
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        item.setText(f"<Bot> {result}")
        self.listWidget.addItem(item)
        self.listWidget.scrollToBottom()


    def exit(self):
        reply = QMessageBox.question(self, '退出', '确定退出？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Chatbot_Window()
    win.show()
    sys.exit(app.exec_())
