import pygame


class Player:
    def __init__(self, name, start_x, start_y):
        self.name = name
        self.start_x = start_x
        self.start_y = start_y
        self.paddle = pygame.Rect(start_x, start_y, 10, 140)
        self.score = 0
        self.speed = 0

    def set_name(self, name):
        self.name = name
