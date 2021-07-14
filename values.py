import pygame
pygame.font.init()

screen_width = 1280
screen_height = 700
game_font = pygame.font.Font("freesansbold.ttf", 32)
name_font = pygame.font.Font("freesansbold.ttf", 20)
error_font = pygame.font.Font("freesansbold.ttf", 48)
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
player_1_name_pos = (900, 10)
player_2_name_pos = (300, 10)
player_1_score_pos = (660, 340)
player_2_score_pos = (600, 340)