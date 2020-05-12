import socket
import traceback

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import threading
import sys
from qt.qt_client import Ui_MainWindow


class Client_Window(QMainWindow, Ui_MainWindow):
    def __init__(self, name):
        super(Client_Window, self).__init__()
        self.setupUi(self)
        self.name = name
        self.IP = "127.0.0.1"
        self.PORT = 33000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.IP, self.PORT))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        self.server.send(self.name.encode(encoding="utf-8"))
        self.textEdit.setFocus()
        self.show()


    def send(self):
        try:
            message = self.textEdit.toPlainText()
            self.textEdit.clear()
            self.textEdit.setFocus()
            self.server.send(message.encode(encoding='utf-8', errors='strict'))
            # add Item
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight)
            font = QtGui.QFont()
            font.setPointSize(12)
            item.setFont(font)
            item.setText(message+" <You>")
            self.listWidget.addItem(item)
            self.listWidget.scrollToBottom()
        except:
            traceback.print_exc()

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                message = self.server.recv(2048).decode("utf8")
                # add Item
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignLeft)
                font = QtGui.QFont()
                font.setPointSize(12)
                item.setFont(font)
                item.setText(message)
                self.listWidget.addItem(item)
                self.listWidget.scrollToBottom()
            except OSError:  # Possibly client has left the chat.
                break

    def exit(self):
        reply = QMessageBox.question(self, '退出', '确定退出？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.send(bytes("{quit}", "utf8"))
            self.server.close()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Client_Window()
    win.show()
    sys.exit(app.exec_())
