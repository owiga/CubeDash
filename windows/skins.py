import pygame
import sys

from settings import *
from resources.button import Button
from resources.button import Button_Sprite
from resources.button import Button_Sprite_skin


class Menu:
    def __init__(self, game):
        self.screen = pygame.display.set_mode((width, height))
        self.outline = pygame.image.load("assets/outline.png")
        self.background = pygame.image.load("assets/fon.png")
        self.game = game
        self.initialize()

    def initialize(self):
        self.buttons = [
            Button_Sprite_skin(self, width // 3 + 140, 400, lambda: 1, "ICON.png", 1, resizemode=2, current=True),
            Button_Sprite_skin(self, width // 3 + 210, 400, lambda: 2, "skin1.png", 2, resizemode=2),
            Button_Sprite_skin(self, width // 3 + 280, 400, lambda: 3, "ICON.png", 3, resizemode=2),
            Button_Sprite_skin(self, width // 3 + 350, 400, lambda: 4, "skin1.png", 4, resizemode=2)]
        self.others_button = [
            Button_Sprite_skin(self, 25, 25, lambda: 55, "back.png", 55),
            Button_Sprite_skin(self, width // 2 - 75, 150, lambda: None, "ICON.png", 99)
        ]

    def update(self):
        self.screen.fill("black")
        self.screen.blit(self.background, (-100, 0))
        self.mousepos = pygame.mouse.get_pos()
        for but in self.others_button:
            but.show()
        for x in self.buttons:
            x.show()
            if x.current:
                self.screen.blit(self.outline, x.rect.topleft)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but.rect.collidepoint(self.mousepos):
                        return but.func()
                for but in self.others_button:
                    if but.rect.collidepoint(self.mousepos):
                        return but.func()
        pygame.display.flip()
        self.game.clock.tick(fps)

    def show(self):
        while True:
            self.update()
            status = self.check_events()
            if status in range(1, 5):
                for but in self.buttons:
                    but.current = False
                    if status == but.numero:
                        but.current = True
                        self.others_button[1].change_image(but.image_name)
            elif status == 55:
                return 55
