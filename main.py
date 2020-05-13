import socket
import traceback

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
import sys

from chatbot import Chatbot_Window
from client_gui import Client_Window
from qt.qt_home import Ui_mainWindow
import matplotlib.pyplot as plt


class Main_Window(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.name = ""
        self.IP = "127.0.0.1"
        self.PORT = 33000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        labels = [self.label_5, self.label_12, self.label_18, self.label_6, self.label_15, self.label_21]
        imgs = ["images/study.jpg", "images/mood.jpg", "images/idea.jpg", "images/relax.jpg", "images/film.jpg", "images/chatbot.jpg"]

        for label, imgs in zip(labels, imgs):
            self.display_image(imgs, label)

        self.show()

    def display_image(self, path_to_img, label):
        input_image = plt.imread(path_to_img)
        height, width, channels = input_image.shape
        bytesPerLine = channels * width
        qImg = QtGui.QImage(input_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap_image = QtGui.QPixmap(QtGui.QPixmap.fromImage(qImg))
        label.setPixmap(pixmap_image)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setScaledContents(True)
        label.setMinimumSize(1, 1)
        label.show()

    def enter(self):
        try:

            text, ok = QInputDialog.getText(self, '输入昵称', '请输入您的昵称：')
            if ok and text == "":
                QMessageBox.information(self, '提示', '昵称不能为空！')
            else:
                self.name = text
                self.server.connect((self.IP, self.PORT))
                self.room = Client_Window(self.name)
                self.room.show()
        except:
            traceback.print_exc()

    def chatbot(self):
        try:

            text, ok = QInputDialog.getText(self, '输入昵称', '请输入您的昵称：')
            if ok and text == "":
                QMessageBox.information(self, '提示', '昵称不能为空！')
            else:
                self.name = text
                self.room = Chatbot_Window(self.name)
                self.room.show()
        except:
            traceback.print_exc()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main_Window()
    win.show()
    sys.exit(app.exec_())
