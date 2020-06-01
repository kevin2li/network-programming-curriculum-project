import sys
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QLineEdit, QMessageBox

from DAO import UserDAO
from qt.qt_LoginWin import Ui_Form
from user import User


class LoginWin(Ui_Form, QtWidgets.QWidget):
    loginSignal = pyqtSignal(str)
    def __init__(self):
        super(LoginWin, self).__init__()
        self.setupUi(self)
        self.lineEdit.setFocus()
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon('images/chatroom_icon.jpg'))
        self.username = ""
        self.pwd = ""
        oImage = QImage("images/background2.jpg")
        sImage = oImage.scaled(QSize(500, 500))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)
        self.setFixedSize(self.width(), self.height())
        self.show()


    def test(self):
        username = self.lineEdit.text()
        pwd = self.lineEdit_2.text()
        if username and pwd:
            print(username, pwd)
            self.username = username
            self.pwd = pwd
            return True
        else:
            QMessageBox.information(self, '提示', '用户名或密码不能为空')
            return False

    def register(self):
        try:
            if self.test():
                dao = UserDAO()
                user = User(self.username, self.pwd)
                username, pwd = dao.retrieveUserByName(user.username)
                if username != "":
                    QMessageBox.information(self, '提示', '用户名已存在！')
                    self.lineEdit.setText("")
                    self.lineEdit_2.setText("")
                else:
                    dao.addUser(user)
                    QMessageBox.information(self, '提示', '注册成功')
        except:
            traceback.print_exc()

    def login(self):
        if self.test():
            dao = UserDAO()
            username, pwd = dao.retrieveUserByName(self.username)
            if username == "" and pwd == "":
                QMessageBox.information(self, '提示', '用户不存在！')
                self.lineEdit_2.setText("")
                self.lineEdit.setText("")
            elif username == self.username and pwd == self.pwd:
                QMessageBox.information(self, '提示', '登录成功！')
                print("登录成功")
                self.loginSignal.emit("login")
                self.close()

            else:
                QMessageBox.information(self, '提示', '用户名或密码错误！')
                print("用户名或密码错误！")
                self.lineEdit_2.setText("")
                self.lineEdit.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginWin()
    win.show()
    sys.exit(app.exec_())