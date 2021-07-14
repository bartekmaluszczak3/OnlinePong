import random
import pygame
import socket
from ball import Ball
from player import Player
from values import screen_width, screen_height, name_font, game_font, bg_color, light_grey, player_1_name_pos, \
    player_2_name_pos, player_1_score_pos, player_2_score_pos
from help_function import create_thread


class Server:
    def __init__(self, host, port, player1_name, player2_name):
        self.host = host
        self.port = port
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.ball = Ball()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.light_grey = (200, 200, 200)
        self.player = Player(player1_name, screen_width - 20, screen_height / 2 - 70)
        self.player_2 = Player(player2_name, 10, screen_height / 2 - 70)
        self.conn = None
        self.addr = None
        self.connection = False
        self.socket.bind((host, port))
        self.socket.listen(1)

    def receive_data(self):
        while self.connection:
            try:
                data = self.conn.recv(1024).decode()
                data = data.split('-')
                self.player_2.paddle.y = int(data[0])
            except:
                self.player_2.paddle.y = 0

    def waiting_for_connection(self):
        self.conn, self.addr = self.socket.accept()
        print("Client connected")
        self.connection = True
        return self.receive_data()

    def check_score(self):
        if self.ball.ball.left <= 0:
            self.player.score += 1
            self.ball.restart()
        if self.ball.ball.right >= screen_width:
            self.player_2.score += 1
            self.ball.restart()

    def reset_game(self):
        self.player.score = 0
        self.player_2.score = 0
        self.ball.ball.center = (screen_width / 2, screen_height / 2)
        self.ball.speed_y *= random.choice((-1, 1))
        self.ball.speed_x *= random.choice((-1, 1))

    def show_error(self):
        self.screen.fill(bg_color)
        caption = game_font.render("Connection lost", False, light_grey)
        self.screen.blit(caption, (500, 300))
        pygame.display.flip()

    def start(self):
        pygame.init()
        clock = pygame.time.Clock()
        create_thread(self.waiting_for_connection)
        pygame.display.set_caption("Server")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player.speed += 3
                    if event.key == pygame.K_UP:
                        self.player.speed -= 3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player.speed -= 3
                    if event.key == pygame.K_UP:
                        self.player.speed += 3
            if self.connection:
                self.player.paddle.y += self.player.speed
                if self.player.paddle.top <= 0:
                    self.player.paddle.top = 0
                if self.player.paddle.bottom >= screen_height:
                    self.player.paddle.bottom = screen_height
                send_data = '{}-{}-{}-{}-{}'.format(self.player.paddle.y, self.ball.ball.x, self.ball.ball.y,
                                                    self.player.score,
                                                    self.player_2.score).encode()
                try:
                    self.conn.send(send_data)
                except Exception as e:
                    self.connection = False

                self.screen.fill(bg_color)
                pygame.draw.rect(self.screen, light_grey, self.player.paddle)
                pygame.draw.rect(self.screen, light_grey, self.player_2.paddle)
                pygame.draw.ellipse(self.screen, light_grey, self.ball.ball)
                pygame.draw.aaline(self.screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
                self.ball.move()
                self.ball.check_collision_player(self.player)
                self.ball.check_collision_opponent(self.player_2)
                self.check_score()
                player_1_score = game_font.render(f"{self.player.score}", False, light_grey)
                player_1_name = name_font.render(self.player.name, False, light_grey)
                player_2_name = name_font.render(self.player_2.name, False, light_grey)
                self.screen.blit(player_1_name, player_1_name_pos)
                self.screen.blit(player_2_name, player_2_name_pos)
                self.screen.blit(player_1_score, player_1_score_pos)
                player_2_score = game_font.render(f"{self.player_2.score}", False, light_grey)
                self.screen.blit(player_2_score, player_2_score_pos)
                clock.tick(60)
                pygame.display.flip()
            else:
                self.show_error()