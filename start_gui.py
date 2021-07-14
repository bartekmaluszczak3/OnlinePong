import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
from client_gui import ClientWindow
from server_gui import ServerWindow

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Ping pong'
        self.left = 500
        self.top = 300
        self.width = 650
        self.height = 400
        self.w = None
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        client = QPushButton('Client', self)
        client.setFont(QFont('Arial', 15))
        client.setToolTip('Select to choose client version')
        client.setGeometry(100, 150, 150, 200)
        client.setStyleSheet("background-color:rgb(255, 104, 104)")
        client.clicked.connect(self.client_click)

        server = QPushButton("Server", self)
        server.setFont(QFont('Arial', 15))
        server.setToolTip("Select to choose server version")
        server.setGeometry(400, 150, 150, 200)
        server.setStyleSheet("background-color:rgb(145, 174, 242)")
        server.clicked.connect(self.server_click)
        self.show()

    @pyqtSlot()
    def client_click(self):
        if self.w is None:
            self.close()
            self.w = ClientWindow()
            self.w.show()

        else:
            self.w.close()
            self.w = None

    @pyqtSlot()
    def server_click(self):
        if self.w is None:
            self.close()
            self.w = ServerWindow()
            self.w.show()

        else:
            self.w.close()
            self.w = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
