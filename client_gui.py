import socket
import threading

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QListWidget
from PyQt5.uic.properties import QtWidgets

from client import Client
from help_function import read_file, save_to_file

class ClientWindow(QWidget):

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
        self.host_history = QListWidget(self)
        self.list_of_hosts = []
        self.init_UI()
        self.start = False

    def init_UI(self):
        self.setWindowTitle("Client")
        self.error_label.setGeometry(200, 20, 350, 30)
        self.error_label.setFont(QFont('Arial', 12))
        self.error_label.setStyleSheet("color: red;")
        history_label = QLabel("History:", self)
        history_label.setFont(QFont('Arial', 8))
        history_label.setGeometry(450, 50, 150, 25)
        self.host_history.setGeometry(450, 75, 150, 200)
        self.list_of_hosts = read_file("client.txt")
        self.host_history.addItems(self.list_of_hosts)
        self.host_history.itemClicked.connect(self.item_selected)

        button = QPushButton('Connect', self)
        button.setFont(QFont('Arial', 8))
        button.setStyleSheet("background-color:rgb(255, 104, 104)")
        button.setGeometry(500, 320, 100, 30)
        button.clicked.connect(self.button_click)

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

    def item_selected(self, item):
        self.host_input.setText(item.text())

    def connection(self):
        print(threading.active_count())
        global server_nick
        nick = self.nick_input.text()
        host = self.host_input.text()
        port = self.port_input.text()
        if host == "" or port == "" or nick == "":
            self.error_label.setText("Any of field can not be blank")
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host not in self.list_of_hosts:
            self.list_of_hosts.append(host)
            self.host_history.addItem(host)
            save_to_file("client.txt", host)
        try:
            sock.connect((host, int(port)))
        except:
            self.error_label.setText("Unable to connect to server")
            return
        try:
            sock.send(nick.encode())
            answer = sock.recv(1024).decode()
            print(answer)
            if answer == "Invalid":
                self.error_label.setText("Username is the same as other player")
            else:
                server_nick = sock.recv(1024).decode()
                self.start = True
        except Exception as e:
            print(e)
            self.error_label.setText("Connection lost")
        print("OK ", self.start)
        if self.start:
            try:
                sock.close()
                self.close()
                client = Client(host, int(port), server_nick, nick)
                client.start()
            except:
                print("client not started")

    def button_click(self):
        self.error_label.setText("")
        thread = threading.Thread(target=self.connection)
        thread.start()
