import pygame
import sys

from settings import *
from resources.button import Button_Sprite


class Table:
    def __init__(self, game):
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load("assets/fon.png")
        self.move_right = False
        self.move_left = False
        self.game = game
        self.initialize()

    def initialize(self):
        self.load = pygame.USEREVENT + 1
        self.buttons = [Button_Sprite(self, 200, 200, lambda: 1, "first.png", resizemode=2),
                        Button_Sprite(self, 1550, 200, lambda: 2, "second.png", resizemode=2),
                        Button_Sprite(self, 25, 25, lambda: 3, "back.png", level=0),
                        Button_Sprite(self, 1440, height // 2 - 35, lambda: 4, "right.png", level=0),
                        Button_Sprite(self, 5, height // 2 - 35, lambda: 5, "left.png", level=0)]

    def update(self):
        self.screen.fill("black")
        self.screen.blit(self.background, (-100, 0))
        self.mousepos = pygame.mouse.get_pos()
        for x in self.buttons:
            x.show()
        if self.move_right:
            if self.buttons[0].rect.x > -1150:
                self.buttons[0].x -= 20
                self.buttons[0].rect.x = self.buttons[0].x
                self.buttons[1].x -= 20
                self.buttons[1].rect.x = self.buttons[1].x
            elif self.buttons[0].rect.x == -1150:
                self.move_right = False
            elif self.buttons[0].rect.x < -1100:
                self.buttons[0].x += 2
                self.buttons[0].rect.x = self.buttons[0].x
                self.buttons[1].x += 2
                self.buttons[1].rect.x = self.buttons[1].x
        elif self.move_left:
            if self.buttons[0].rect.x < 200:
                self.buttons[0].x += 20
                self.buttons[0].rect.x = self.buttons[0].x
                self.buttons[1].x += 20
                self.buttons[1].rect.x = self.buttons[1].x
            elif self.buttons[0].rect.x == 200:
                self.move_left = False
            elif self.buttons[0].rect.x > 200:
                self.buttons[0].x -= 2
                self.buttons[0].rect.x = self.buttons[0].x
                self.buttons[1].x -= 2
                self.buttons[1].rect.x = self.buttons[1].x

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but.rect.collidepoint(self.mousepos):
                        if but.level != 0:
                            play.play()
                            self.load = pygame.USEREVENT + 1
                            pygame.time.set_timer(self.load, 1000)
                            main_menu.stop()
                            self.butfunc = but.func()
                        else:
                            return but.func()
            if event.type == self.load:
                pygame.time.set_timer(self.load, 0)
                return self.butfunc
        pygame.display.flip()
        self.game.clock.tick(fps)

    def show(self):
        while True:
            status = self.check_events()
            if status == 1:
                return 1
            elif status == 2:
                return 2
            elif status == 3:
                return 3
            elif status == 4:
                self.move_right = True
                self.move_left = False
            elif status == 5:
                self.move_left = True
                self.move_right = False
            self.update()
