from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from login import LoginWin
from main import Main_Window


class ViewController:
    def loadLoginView(self):
        self.viewlogin = LoginWin()
        self.viewlogin.loginSignal.connect(self.loadMainWinView)
        self.viewlogin.show()

    def loadMainWinView(self, str):
        self.viewMainWIn = Main_Window()
        self.viewMainWIn.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = ViewController()
    view.loadLoginView()
    sys.exit(app.exec_())
