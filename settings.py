import sys

import pygame

pygame.init()
width = 1600
height = 900
fps = 62
GRAVITY = 15
font = pygame.font.SysFont("ArialBlack", 15)
blocks = {
    1: "assets/spike.png",
    21: "assets/block.png",
    20: "assets/pol.png",
    22: "assets/pol2.png",
    19: "assets/polu_block.png",
    2: "assets/spikeL.png",
    3: "assets/mspike.png"
}


def terminate():
    pygame.quit()
    sys.exit()


def fps_counter(clock, screen):
    fpsy = str(int(clock.get_fps()))
    fps_t = font.render(fpsy, 1, pygame.Color("GREEN"))
    screen.blit(fps_t, (10, 0))

