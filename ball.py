import random

import pygame

screen_width = 1280
screen_height = 700


class Ball:
    def __init__(self):
        self.ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.ball.x += self.speed_x
        self.ball.y += self.speed_y
        if self.ball.top <= 0 or self.ball.bottom >= screen_height:
            self.speed_y *= -1

    def check_collision_player(self, player):
        if self.ball.colliderect(player.paddle) and self.speed_x > 0:
            if abs(self.ball.right - player.paddle.left) < 10:
                self.speed_x *= -1
            elif abs(self.ball.bottom - player.paddle.top) < 10 and self.speed_y > 6:
                self.speed_y *= -1

    def check_collision_opponent(self, player):
        if self.ball.colliderect(player.paddle) and self.speed_x < 0:
            if abs(self.ball.left - player.paddle.right) < 10:
                self.speed_x *= -1
            elif abs(self.ball.top - player.paddle.top) < 10 and self.speed_y < 0:
                self.speed_y *= -1


    def restart(self):
        self.ball.center = (screen_width / 2, screen_height / 2)
        self.speed_y *= random.choice((-1, 1))
        self.speed_x *= random.choice((-1, 1))
