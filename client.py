import pygame
import socket
from ball import Ball
from player import Player
from help_function import create_thread
from values import screen_width, screen_height, name_font, game_font, bg_color, light_grey, player_1_name_pos,\
    player_2_name_pos, player_1_score_pos, player_2_score_pos


class Client:
    def __init__(self, host, port, player1_name, player2_name):
        self.host = host
        self.port = port
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.ball = Ball()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = Player(player1_name, screen_width - 20, screen_height / 2 - 70)
        self.player_2 = Player(player2_name, 10, screen_height / 2 - 70)

    def receive_data(self):
        while True:
            data = self.socket.recv(1024).decode()
            data = data.split('-')
            try:
                self.player.paddle.y = int(data[0])
                self.ball.ball.x = int(data[1])
                self.ball.ball.y = int(data[2])
                self.player.score = int(data[3])
                self.player_2.score = int(data[4])

            except:
                self.ball.ball.y = 0

    def start(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Client')
        try:
            self.socket.connect((self.host, self.port))
        except:
            print("Connection failed")
        create_thread(self.receive_data)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player_2.speed += 3
                    if event.key == pygame.K_UP:
                        self.player_2.speed -= 3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player_2.speed -= 3
                    if event.key == pygame.K_UP:
                        self.player_2.speed += 3

            self.player_2.paddle.y += self.player_2.speed
            if self.player_2.paddle.top <= 0:
                self.player_2.paddle.top = 0
            if self.player_2.paddle.bottom >= screen_height:
                self.player_2.paddle.bottom = screen_height
            send_data = '{}'.format(self.player_2.paddle.y).encode()
            self.socket.send(send_data)
            self.screen.fill(bg_color)
            pygame.draw.rect(self.screen, light_grey, self.player.paddle)
            pygame.draw.rect(self.screen, light_grey, self.player_2.paddle)
            pygame.draw.ellipse(self.screen, light_grey, self.ball.ball)
            pygame.draw.aaline(self.screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
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
