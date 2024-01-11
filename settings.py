import sys

import pygame

pygame.init()
width = 1600
height = 900
fps = 60
font = pygame.font.SysFont("ArialBlack", 15)


def terminate():
    pygame.quit()
    sys.exit()


def fps_counter(clock, screen):
    fpsy = str(int(clock.get_fps()))
    fps_t = font.render(fpsy, 1, pygame.Color("RED"))
    screen.blit(fps_t, (10, 0))
