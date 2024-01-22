import pygame
import sys

from settings import *
from resources.button import Button_Sprite


class MainMenu:
    def __init__(self, game):
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load("assets/fon.png")
        self.title = pygame.image.load("assets/title.png")
        self.credits = pygame.image.load("assets/info.png")
        self.info_show = False
        self.game = game
        self.x, self.y = 335, 200
        self.initialize()

    def initialize(self):
        self.buttons = [
            Button_Sprite(self, width // 2 + 90, height // 2 - 95, lambda: 1, "play_button.png", resizemode=2),
            Button_Sprite(self, width // 2 - 245, height // 2 - 95, lambda: 2, "skin_button.png", resizemode=2),
            Button_Sprite(self, width // 2 - 200, height - 170, lambda: 9, "music.png", level=2),
            Button_Sprite(self, width // 2 + 90, height - 170, lambda: 10, "sound.png", level=3),
            Button_Sprite(self, 30, 30, lambda: 7, "shutdown.png"),
            Button_Sprite(self, 30, height - 170, lambda: 8, "credits.png")]

    def print_text(self):
        with open("credits.txt", "r", encoding="utf8") as file:
            for text in file.readlines():
                self.game.screen.blit(font4.render(text.strip(), 1, pygame.Color("white")), (self.x, self.y))
                self.y += 30
                if self.y == 350:
                    self.y = 200

    def update(self):
        self.screen.blit(self.background, (-100, 0))
        self.screen.blit(self.title, (200, 50))
        self.mousepos = pygame.mouse.get_pos()
        for x in self.buttons:
            x.show()
        if self.info_show:
            self.game.screen.blit(self.credits, (300, 0))
            self.print_text()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but.rect.collidepoint(self.mousepos):
                        return but.func(), but.level
        pygame.display.flip()
        self.game.clock.tick(fps)

    def show(self):
        with open("data/sound_signals.txt", mode="w") as file:
            file.write("0.2" + " " + "0.2")
        while True:
            status = self.check_events()
            try:
                if status[0] == 9:
                    if main_menu.get_volume() % 2 != 0:
                        main_menu.set_volume(volume[0])
                        jumper_music.set_volume(volume[0])
                        theory_of_madness_music.set_volume(volume[0])
                        self.buttons[status[1]].change_image("music_offed.png")
                    else:
                        main_menu.set_volume(volume[1])
                        jumper_music.set_volume(volume[1])
                        theory_of_madness_music.set_volume(volume[1])
                        self.buttons[status[1]].change_image("music.png")
                elif status[0] == 10:
                    if play.get_volume() % 2 != 0:
                        play.set_volume(volume[0])
                        death.set_volume(volume[0])
                        win.set_volume(volume[0])
                        self.buttons[status[1]].change_image("sound_offed.png")
                    else:
                        play.set_volume(volume[1])
                        death.set_volume(volume[1])
                        win.set_volume(volume[1])
                        self.buttons[status[1]].change_image("sound.png")
                elif status[0] == 8:
                    self.info_show = not self.info_show
                elif not status[0] is None and status[0] not in range(8, 11):
                    break
                with open("data/sound_signals.txt", mode="w") as file:
                    file.write(
                        str(round(play.get_volume(), 1)) + " " + str(round(main_menu.get_volume(), 1)))
            except TypeError:
                pass
            self.update()
        return status[0]
