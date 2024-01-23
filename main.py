from settings import *
from resources.player import Player
from resources.button import Button_Sprite_Win, Button_Sprite
from resources.block import Block
from resources.camera import Camera
from resources.win_table import WinTable
from resources.text import Attempt, Name_level
from levels import level
from windows import menu
from windows import skins
from windows import levels


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.progress_add = 0.048

        self.offset_x = 0
        self.bx = -100
        self.attempts = 1
        self.mousepos = (0, 0)
        self.progress = 0
        self.num_level = 1
        self.counter = 0

        self.blocks = pygame.sprite.Group()
        self.players = pygame.sprite.GroupSingle()
        self.particles = pygame.sprite.Group()
        self.death_particles = pygame.sprite.Group()
        self.Table = pygame.sprite.GroupSingle()
        self.Table_Buttons = pygame.sprite.Group()

        self.buttons = [
            Button_Sprite_Win(self, 400, -200, lambda: 3, "menu.png"),
            Button_Sprite_Win(self, 1050, -200, lambda: 6, "restart.png"),
            Button_Sprite(self, width // 2 - 200, -300, lambda: 9, "music.png"),
            Button_Sprite(self, width // 2 + 90, -300, lambda: 10, "sound.png")
        ]
        self.menu = self.buttons[0]
        self.restart = self.buttons[1]
        self.music_b = self.buttons[2]
        self.sound_b = self.buttons[3]

        self.player = Player(self)
        self.camera = Camera(self)
        self.win_table = WinTable(self)
        self.level_name = Name_level(self)

        self.enabled = True
        self.win = False
        self.checker = False
        self.win_table_show = False
        self.move_table = False
        self.pause = False

        self.attempt = None
        self.win_coords = None
        self.map_level = None
        self.startpos = None
        self.current_music = None
        self.current_level = None

        self.pulse_event = pygame.USEREVENT + 2
        self.change_bg_event = pygame.USEREVENT + 3
        self.win_event = pygame.USEREVENT + 4
        self.done_event = pygame.USEREVENT + 5

        self.background = pygame.image.load("assets/fon.png")
        self.background2 = pygame.image.load("assets/fon.png")
        self.start_back = pygame.image.load("assets/fon.png")
        self.pause_image = pygame.image.load("assets/pause.png")

        with open("data/current_skin.txt", mode="r") as file:
            self.current_skin = int(file.readline())

        main_menu.play(-1)

    def game(self, num_level):
        with open("data/current_skin.txt", mode="r") as file:
            self.player.change_skin(int(file.readline()))

        with open("data/sound_signals.txt", mode="r") as file:
            status = file.readline().split()
            self.sound_b.change_image(image_sounds.get(status[0]))
            self.music_b.change_image(image_musics.get(status[1]))

        self.attempts = 1
        self.progress = 0

        self.checker = False
        self.pause = False
        self.win = False

        self.num_level = num_level
        self.startpos = [0, 670]
        self.player.rect.topleft = self.startpos

        main_menu.stop()

        if num_level == 1:
            self.current_level = "Theory of Madness"
            self.progress_add = progress_adding.get(self.num_level)
            self.map_level = level.level(num_level)
            self.current_music = theory_of_madness_music.play()
            self.load_level(self.map_level)
            self.background2 = pygame.image.load("assets/fon.png")
            self.background = pygame.image.load("assets/fon.png")
            self.start_back = pygame.image.load("assets/fon.png")

        elif num_level == 2:
            self.current_level = "Jumper"
            self.progress_add = progress_adding.get(self.num_level)
            self.map_level = level.level(num_level)
            self.current_music = jumper_music.play()
            self.load_level(self.map_level)
            self.background2 = pygame.image.load("assets/fon2.png")
            self.background = pygame.image.load("assets/fon2.png")
            self.start_back = pygame.image.load("assets/fon2.png")

    def procent(self):
        current_procent = str(round(self.progress, 1)) + "%"
        text = font2.render(current_procent, 1, pygame.Color("WHITE"))
        self.screen.blit(text, (width // 2 - 10, 0))

    def update(self):
        self.screen.fill("black")
        self.screen.blit(self.background, (self.bx, 0))
        self.screen.blit(self.background2, (self.bx + 1800, 0))

        self.blocks.draw(self.screen)
        self.blocks.update(self.offset_x)
        self.players.draw(self.screen)
        self.particles.draw(self.screen)
        self.death_particles.draw(self.screen)
        self.death_particles.update()
        self.Table.draw(self.screen)
        self.Table.update(self.offset_x)
        self.attempt.update()

        self.mousepos = pygame.mouse.get_pos()

        if self.background.get_alpha() != 255:
            self.background.set_alpha(self.background.get_alpha() + 5)
            self.background2.set_alpha(self.background.get_alpha() + 5)

        if not self.pause or not self.checker:
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
        elif self.pause:
            self.current_music.pause()

            self.screen.blit(self.pause_image, (300, 50))
            self.level_name.show()

        fps_counter(self.clock, self.screen)
        self.menu.show()
        self.restart.show()
        self.music_b.show()
        self.sound_b.show()
        self.procent()
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
                self.players.empty()

        if self.win_table_show:
            self.screen.blit(self.win_table.total_jumps_text, (self.win_table.rect.x + 100,
                                                               self.win_table.rect.y + 340))
            self.screen.blit(self.win_table.total_attempts_text, (self.win_table.rect.x + 100,
                                                                  self.win_table.rect.y + 290))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.win_table_show:
                    self.pause = not self.pause
                    self.checker = not self.checker

                    if self.pause:
                        self.restart.rect.topleft = (605, 400)
                        self.menu.rect.topleft = (838, 400)
                        self.music_b.rect.topleft = (367, 400)
                        self.sound_b.rect.topleft = (1076, 400)
                    else:
                        self.music_b.rect.topleft = (838, -400)
                        self.sound_b.rect.topleft = (800, -400)
                        self.restart.rect.topleft = (1050, -200)
                        self.menu.rect.topleft = (400, -200)

            if event.type == self.pulse_event and not self.pause:
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

            elif event.type == self.win_event:  # Когда перешел вин ивент
                self.progress = 100
                self.player.speedx = 0

                self.checker = True
                self.player.particle_enable = False
                self.win = True

                self.particles.empty()
                self.player.kill()
                self.current_music.stop()
                win.play()

                pygame.time.set_timer(self.win_event, 0)
                pygame.time.set_timer(self.done_event, 3000)

            elif event.type == self.done_event:  # Таблица победа
                self.move_table = True
                pygame.time.set_timer(self.done_event, 0)

            if event.type == self.player.death_event:
                pygame.time.set_timer(self.player.death_event, 0)

                self.progress = 0
                self.bx = -100
                self.player.speedx = 10

                self.player.add(self.players)
                self.blocks.empty()
                self.death_particles.empty()

                self.load_level(self.map_level)
                self.background2 = self.start_back
                self.background = self.start_back
                self.player.rect.topleft = self.startpos

                if not self.checker:
                    levels_musics.get(self.num_level).play()
                else:
                    self.player.music_offed = True

                self.player.died = False
                self.player.particle_enable = True
                self.progress_add = progress_adding.get(self.num_level)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but.rect.collidepoint(self.mousepos):
                        return but.func()

        pygame.display.update()
        self.clock.tick(fps)

    def load_level(self, map_level):
        x, y = 1 - self.camera.offset, 0

        for row in map_level:
            for element in row:
                self.block_build(element, x, y)
                x += 70
            y += 70
            x = 0

    def block_build(self, name, x, y):
        if name == "w2":
            self.win_coords = (x, y)
        elif name == "t":
            self.attempt = Attempt(self, x, y)
            return
        elif name != '_' and name != '':
            Block(self, (x, y), blocks_names.get(name))


    def restart_level(self):
        self.players.empty()
        self.particles.empty()
        self.blocks.empty()
        self.death_particles.empty()

        self.player.add(self.players)
        self.player.speedx = 10
        self.player.jumps = 0

        pygame.time.set_timer(self.pulse_event, 0)

        self.win_table_show = False
        self.win_table.restart_game()
        self.current_music.stop()
        self.player.died = False
        self.player.particle_enable = True
        self.background2 = self.start_back
        self.background = self.start_back
        self.progress_add = progress_adding.get(self.num_level)
        self.game(self.num_level)

    def run(self):
        self.enabled = True
        while self.enabled:
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
                elif status == 7:
                    terminate()
            while True:
                status = self.check_events()
                self.update()
                if status == 3:
                    self.win_table.restart_game()
                    self.enabled = False
                    break
                elif status == 6:
                    self.restart_level()
                elif status == 9:
                    if main_menu.get_volume() % 2 != 0:
                        main_menu.set_volume(volume[0])
                        jumper_music.set_volume(volume[0])
                        theory_of_madness_music.set_volume(volume[0])
                        self.music_b.change_image("music_offed.png")
                    else:
                        main_menu.set_volume(volume[1])
                        jumper_music.set_volume(volume[1])
                        theory_of_madness_music.set_volume(volume[1])
                        self.music_b.change_image("music.png")
                elif status == 10:
                    if play.get_volume() % 2 != 0:
                        play.set_volume(volume[0])
                        death.set_volume(volume[0])
                        win.set_volume(volume[0])
                        self.sound_b.change_image("sound_offed.png")
                    else:
                        play.set_volume(volume[1])
                        death.set_volume(volume[1])
                        win.set_volume(volume[1])
                        self.sound_b.change_image("sound.png")


if __name__ == '__main__':
    while True:
        while True:
            game = Game()
            game.run()
