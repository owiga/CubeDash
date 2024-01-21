import sys

import pygame

pygame.init()
procent = 100
width = 1600
height = 900
fps = 60
GRAVITY = 15
font = pygame.font.SysFont("ArialBlack", 15)
font_Procents = pygame.font.SysFont("ArialBlack", 30)
blocks = {
    1: "assets/spike.png",
    21: "assets/block.png",
    20: "assets/pol.png",
    22: "assets/pol2.png",
    19: "assets/polu_block.png",
    2: "assets/spikeL.png",
    3: "assets/mspike.png",
    4: "assets/spikeU.png",
    5: "assets/spiker.png",
    6: "assets/mspiker.png",
    99: "assets/event_line.png",
    98: "assets/event_line.png",
    97: "assets/event_line.png",
    96: "assets/event_line.png"
}

main_menu = pygame.mixer.Sound("sounds/mainmenu.wav")
main_menu.set_volume(0.05)
death = pygame.mixer.Sound("sounds/death.wav")
death.set_volume(0.1)
jumper_music = pygame.mixer.Sound("sounds/jumper.wav")
jumper_music.set_volume(0.2)
theory_of_madness_music = pygame.mixer.Sound("sounds/theoryofeverything.wav")
theory_of_madness_music.set_volume(0.2)
levels_musics = {
    1: theory_of_madness_music,
    2: jumper_music
}
play = pygame.mixer.Sound("sounds/play.wav")
play.set_volume(0.2)
win = pygame.mixer.Sound("sounds/win.wav")
win.set_volume(0.5)

angles = [0, -90, -180, -270, -360]


def terminate():
    pygame.quit()
    sys.exit()


def fps_counter(clock, screen):
    fpsy = str(int(clock.get_fps()))
    fps_t = font.render(fpsy, 1, pygame.Color("GREEN"))
    screen.blit(fps_t, (10, 0))
