import socket
import traceback
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox, QLabel, QDialogButtonBox, QLineEdit, \
    QDialog, QFormLayout
import sys
from chatbot import Chatbot_Window
from client_gui import Client_Window
from qt.qt_home import Ui_mainWindow
import matplotlib.pyplot as plt


class InputDialog(QDialog):
    def __init__(self, host="127.0.0.1", port="33000", nickname=""):
        super(InputDialog, self).__init__()
        self.setWindowTitle("配置")
        self.setWindowIcon(QIcon('images/chatroom_icon.jpg'))

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        self.third = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        self.first.setText(str(host))
        self.second.setText(str(port))
        self.third.setText(str(nickname))

        layout = QFormLayout(self)
        layout.addRow("服务器地址:", self.first)
        layout.addRow("端口号:", self.second)
        layout.addRow("昵称:", self.third)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return self.first.text(), self.second.text(), self.third.text()


class Main_Window(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.IP = "127.0.0.1"
        self.PORT = 33000
        self.server = ""
        self.nickname = ""
        self.room = ""
        labels = [self.label_5, self.label_12, self.label_18, self.label_6, self.label_15, self.label_21]
        imgs = ["study.jpg", "mood.jpg", "idea.jpg", "relax.jpg", "film.jpg", "chatbot.jpg"]

        for label, imgs in zip(labels, imgs):
            self.display_image("images/" + imgs, label)
        self.setWindowIcon(QIcon('images/chatroom_icon.jpg'))
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
        if self.nickname == "":
            text, ok = QInputDialog.getText(self, '输入昵称', '请输入您的昵称：')
            if ok:
                if text == "":
                    QMessageBox.information(self, '提示', '昵称不能为空！')
                else:
                    self.nickname = text
            else:
                return
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((self.IP, self.PORT))
        except:
            traceback.print_exc()
            QMessageBox.information(self, '提示', '无法连接服务器')
        self.room = Client_Window(self.nickname, self.server)
        self.room.show()

    def chatbot(self):
        try:
            if self.nickname == "":
                text, ok = QInputDialog.getText(self, '输入昵称', '请输入您的昵称：')
                if ok:
                    if text == "":
                        QMessageBox.information(self, '提示', '昵称不能为空！')
                    else:
                        self.nickname = text
                else:
                    return
            self.room = Chatbot_Window(self.nickname)
            self.room.show()
        except:
            traceback.print_exc()

    def config(self):
        try:
            self.configDialog = InputDialog(self.IP, self.PORT, self.nickname)
            if self.configDialog.exec_():
                host, port, nickname = self.configDialog.getInputs()
                if host and port and nickname:
                    self.IP, self.PORT, self.nickname = host, int(port), nickname
                else:
                    QMessageBox.information(self, '提示', '信息不能为空！')
        except:
            traceback.print_exc()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main_Window()
    win.show()
    sys.exit(app.exec_())
