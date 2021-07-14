import random
import socket
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QListWidget
import threading

from help_function import read_file, save_to_file
from server import Server


class ServerWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 500
        self.top = 300
        self.width = 650
        self.height = 400
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.nick_input = QLineEdit(self)
        self.host_input = QLineEdit(self)
        self.port_input = QLineEdit(self)
        self.error_label = QLabel("", self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setWindowTitle("Server")
        self.host_history = QListWidget(self)
        self.list_of_hosts = []
        self.init_UI()
        self.start = False
    def init_UI(self):
        self.error_label.setGeometry(200, 20, 250, 30)
        self.error_label.setFont(QFont('Arial', 12))
        self.error_label.setStyleSheet("color: red;")

        button = QPushButton('Start', self)
        button.setFont(QFont('Arial', 8))
        button.setStyleSheet("background-color:rgb(145, 174, 242)")
        button.setGeometry(500, 320, 100, 30)
        button.clicked.connect(self.button_click)

        history_label = QLabel("History:", self)
        history_label.setFont(QFont('Arial', 8))
        history_label.setGeometry(450, 50, 150, 25)
        self.host_history.setGeometry(450, 75, 150, 200)
        self.list_of_hosts = read_file("server.txt")
        self.host_history.addItems(self.list_of_hosts)
        self.host_history.itemClicked.connect(self.item_selected)

        nick_label = QLabel("Nick:", self)
        nick_label.setGeometry(50, 75, 100, 25)
        nick_label.setFont(QFont('Arial', 10))
        self.nick_input.setGeometry(50, 110, 150, 25)

        host_label = QLabel("Host:", self)
        host_label.setGeometry(50, 150, 100, 25)
        host_label.setFont(QFont('Arial', 10))
        self.host_input.setGeometry(50, 185, 150, 25)

        port_label = QLabel("Port:", self)
        port_label.setGeometry(50, 225, 100, 25)
        port_label.setFont(QFont('Arial', 10))
        self.port_input.setGeometry(50, 260, 100, 25)
        self.random_port()
        self.port_input.setReadOnly(True)

    def random_port(self):
        self.port_input.setText(str(random.randint(1000, 6000)))

    def item_selected(self, item):
        self.host_input.setText(item.text())

    def connection(self):
        nick = self.nick_input.text()
        host = self.host_input.text()
        port = self.port_input.text()
        if host == "" or port == "" or nick == "":
            self.error_label.setText("Any of field can not be blank")
            return
        if host not in self.list_of_hosts:
            self.list_of_hosts.append(host)
            self.host_history.addItem(host)
            save_to_file("server.txt", host)
        self.sock.bind((host, int(port)))
        self.sock.listen(1)
        self.error_label.setText("Start listening")
        while not self.start:
            conn, addr = self.sock.accept()
            client_nick = conn.recv(1024).decode()
            if client_nick == nick:
                try:
                    conn.send("Invalid".encode())
                except:
                    print("Invalid")

            else:
                conn.send("Ok".encode())
                conn.send(nick.encode())
                self.start = True
        self.sock.close()
        server = Server(host, int(port), nick, client_nick)
        server.start()

    def button_click(self):
        self.error_label.setText("")
        thread = threading.Thread(target=self.connection)
        thread.start()
