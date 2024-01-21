import sys
import pygame

from settings import *
from resources.player import Player
from resources.block import Block
from resources.camera import Camera
from levels import level
from windows import menu
from windows import skins
from windows import levels


class Game:
    def __init__(self):
        self.startpos = None
        self.progress_add = 0.048
        pygame.init()
        self.checker = False
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.offset_x = 0
        self.bx = -100
        self.blocks = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.death_particles = pygame.sprite.Group()
        self.player = Player(self)
        self.camera = Camera(self)
        self.progress = 0
        self.num_level = 1
        self.current_music = None
        self.win = False
        self.counter = 0
        self.pulse_event = pygame.USEREVENT + 2
        self.change_bg_event = pygame.USEREVENT + 3
        self.win_event = pygame.USEREVENT + 4
        self.done_event = pygame.USEREVENT + 5
        self.start_back = pygame.image.load("assets/fon.png")
        main_menu.play(-1)

    def game(self, num_level):
        self.num_level = num_level
        self.startpos = [0, 670]
        main_menu.stop()
        if num_level == 1:
            self.progress_add = 0.048
            self.map_level = level.level(num_level)
            self.current_music = theory_of_madness_music.play()
            self.load_level(self.map_level)
            self.background2 = pygame.image.load("assets/fon.png")
            self.background = pygame.image.load("assets/fon.png")
            self.start_back = pygame.image.load("assets/fon.png")
        elif num_level == 2:
            self.progress_add = 0.04
            self.map_level = level.level(num_level)
            self.current_music = jumper_music.play()
            self.load_level(self.map_level)
            self.background2 = pygame.image.load("assets/fon2.png")
            self.background = pygame.image.load("assets/fon2.png")
            self.start_back = pygame.image.load("assets/fon2.png")

    def coords(self):
        procent = str(round(self.progress, 1)) + "%"
        text = font_Procents.render(procent, 1, pygame.Color("WHITE"))
        self.screen.blit(text, (width // 2 - 10, 0))

    def update(self):
        self.screen.fill("black")
        self.screen.blit(self.background, (self.bx, 0))
        self.screen.blit(self.background2, (self.bx + 1800, 0))
        self.blocks.update(self.offset_x)
        self.blocks.draw(self.screen)
        self.players.draw(self.screen)
        self.particles.draw(self.screen)
        self.death_particles.draw(self.screen)
        self.death_particles.update()
        if self.background.get_alpha() != 255:
            self.background.set_alpha(self.background.get_alpha() + 5)
            self.background2.set_alpha(self.background.get_alpha() + 5)
        if not self.checker:
            self.player.update_(self.offset_x)
            if self.player.music_offed:
                self.current_music = levels_musics.get(self.num_level).play()
                self.player.music_offed = False
            else:
                self.current_music.unpause()
            self.particles.update()
            self.progress += self.progress_add
            if int(self.progress) == 100:
                self.progress_add = 0
        else:
            self.current_music.pause()
        fps_counter(self.clock, self.screen)
        self.coords()
        self.camera.update()
        if self.win:
            self.current_music.unpause()
            if self.player.image.get_alpha() > 0:
                self.player.image.set_alpha(self.player.image.get_alpha() - 15)
            if self.player.rect.x <= self.win_coords[0]:
                self.player.rect.x += 7
            if self.player.rect.y >= self.win_coords[1]:
                self.player.rect.y -= 4
            if self.player.rect.x >= self.win_coords[0] and self.player.rect.y <= self.win_coords[1]:
                self.win = False
                self.checker = False
                self.players.empty()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.checker = not self.checker
            if event.type == self.pulse_event:
                self.counter += 1
                if self.counter % 2 == 1:
                    self.background = pygame.image.load("assets/fon2.png")
                    self.background2 = pygame.image.load("assets/fon2.png")
                else:
                    self.background = pygame.image.load("assets/fon.png")
                    self.background2 = pygame.image.load("assets/fon.png")
            elif event.type == self.change_bg_event:
                self.background.set_alpha(120)
                self.background2.set_alpha(120)
                self.counter += 1
                if self.counter % 2 == 1:
                    self.background = pygame.image.load("assets/fon.png")
                    self.background2 = pygame.image.load("assets/fon.png")
                else:
                    self.background = pygame.image.load("assets/fon2.png")
                    self.background2 = pygame.image.load("assets/fon2.png")
                self.background.set_alpha(120)
                self.background2.set_alpha(120)
                pygame.time.set_timer(self.change_bg_event, 0)
            elif event.type == self.win_event:
                self.checker = True
                self.player.particle_enable = False
                self.particles.empty()
                self.win = True
                self.player.speedx = 0
                win.play()
                pygame.time.set_timer(self.win_event, 0)
                pygame.time.set_timer(self.done_event, 100)
            elif event.type == self.done_event:
                levels_musics.get(self.num_level).set_volume(0.05)
                pygame.time.set_timer(self.done_event, 0)
            if event.type == self.player.death_event:
                self.player.await_ev = False
                pygame.time.set_timer(self.player.death_event, 0)
                self.player.add(self.players)
                self.progress = 0
                self.player.speedx = 10
                self.blocks.empty()
                self.load_level(self.map_level)
                self.bx = -100
                self.player.rect.topleft = self.startpos
                if not self.checker:
                    levels_musics.get(self.num_level).play()
                else:
                    self.player.music_offed = True
                self.death_particles.empty()
                self.player.died = False
                self.player.particle_enable = True
                self.background2 = self.start_back
                self.background = self.start_back

        pygame.display.flip()
        self.clock.tick(fps)

    def load_level(self, level):
        self.x, y = 1 - self.camera.offset, 0
        for row in level:
            for element in row:
                if element == "b":
                    Block(self, (self.x, y), 21)
                elif element == "s":
                    Block(self, (self.x, y), 1)
                elif element == "sl":
                    Block(self, (self.x, y), 2)
                elif element == "ms":
                    Block(self, (self.x, y), 3)
                elif element == "p":
                    Block(self, (self.x, y), 20)
                elif element == "p2":
                    Block(self, (self.x, y), 22)
                elif element == "pb":
                    Block(self, (self.x, y), 19)
                elif element == "su":
                    Block(self, (self.x, y), 4)
                elif element == "sr":
                    Block(self, (self.x, y), 5)
                elif element == "msu":
                    Block(self, (self.x, y), 6)
                elif element == "be":
                    Block(self, (self.x, y), 99)
                elif element == "bec":
                    Block(self, (self.x, y), 98)
                elif element == "w":
                    Block(self, (self.x, y), 97)
                elif element == "w2":
                    Block(self, (self.x, y), 96)
                    self.win_coords = (self.x, y)
                self.x += 70
            y += 70
            self.x = 0

    def run(self):
        while True:
            status = menu.MainMenu(self).show()
            if status == 1:
                code_feedback = levels.Table(self).show()
                if code_feedback == 1:
                    self.game(1)
                    break
                elif code_feedback == 2:
                    self.game(2)
                    break
            elif status == 2:
                skins.Menu(self).show()
        while True:
            self.check_events()
            self.update()


if __name__ == '__main__':
    game = Game()
    game.run()
