import json
import socket
import traceback

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import threading
import sys

from message import Message
from qt.qt_client import Ui_MainWindow


class Client_Window(QMainWindow, Ui_MainWindow):
    def __init__(self, name, server):
        super(Client_Window, self).__init__()
        self.setupUi(self)
        self.name = name
        self.IP = "127.0.0.1"
        self.PORT = 33000
        # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server.connect((self.IP, self.PORT))
        self.server = server

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        self.server.send(self.name.encode(encoding="utf-8"))
        self.lineEdit.setFocus()
        self.setWindowIcon(QIcon('images/chatroom_icon.jpg'))
        self.show()


    def send(self):
        try:
            text = self.lineEdit.text()
            message = Message("msg", text, self.name).serialize()
            self.lineEdit.clear()
            self.lineEdit.setFocus()
            self.server.send(message.encode(encoding='utf-8', errors='strict'))
            # add Item
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight)
            font = QtGui.QFont()
            font.setPointSize(12)
            item.setFont(font)
            item.setText(text+" <You>")
            self.listWidget.addItem(item)
            self.listWidget.scrollToBottom()
        except:
            traceback.print_exc()

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                message = self.server.recv(2048).decode("utf-8")
                message = json.loads(message)
                if message['type'] == "join":
                    item = QtWidgets.QListWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignLeft)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    item.setFont(font)
                    item.setText(f"<{message['sender']}> {message['content']} has joined the chat!")
                    self.listWidget.addItem(item)
                    self.listWidget_2.addItem(message['content'])
                elif message['type'] == "leave":
                    item = QtWidgets.QListWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignLeft)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    item.setFont(font)
                    item.setText(f"<{message['sender']}> {message['content']} has left the chat.")
                    self.listWidget.addItem(item)

                elif message['type'] == "member":
                    self.listWidget_2.clear()
                    names = eval(message['content'])
                    for name in names:
                        if name != self.name:
                            self.listWidget_2.addItem(name)
                        else:
                            self.listWidget_2.addItem(name + "<You>")
                else:
                    # add Item
                    item = QtWidgets.QListWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignLeft)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    item.setFont(font)
                    item.setText(f"<{message['sender']}> {message['content']}")
                    self.listWidget.addItem(item)
                    self.listWidget.scrollToBottom()
            except OSError:  # Possibly client has left the chat.
                break

    def exit(self):
        reply = QMessageBox.question(self, '退出', '确定退出？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            msg = Message("leave", "", self.name)
            self.server.send(msg.serialize().encode(encoding="utf-8"))
            self.server.shutdown(2)
            self.server.close()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Client_Window("Kevin")
    win.show()
    sys.exit(app.exec_())
