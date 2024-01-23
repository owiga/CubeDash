from settings import *


class WinTable(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.x = 300
        self.y = -750
        self.game = game
        self.image = pygame.image.load("assets/win.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.total_jumps = f"Total jumps - {self.game.player.jumps}"
        self.total_attempts = f"Total attempts - {self.game.attempts}"
        self.total_jumps_text = font2.render(self.total_jumps, 1, "white")
        self.total_attempts_text = font2.render(self.total_attempts, 1, "white")
        self.add(self.game.Table)

    def restart_game(self):
        self.rect.topleft = (self.x, self.y)
        self.game.restart.rect.y = -200
        self.game.menu.rect.y = -200

    def update(self, offset):
        self.total_jumps = f"Total jumps - {self.game.player.jumps}"
        self.total_attempts = f"Total attempts - {self.game.attempts}"
        self.total_jumps_text = font2.render(self.total_jumps, 1, "white")
        self.total_attempts_text = font2.render(self.total_attempts, 1, "white")
        self.rect.x += offset
        if self.game.move_table:
            if self.rect.y < 0:
                self.rect.y += 25
                self.game.screen.blit(self.total_jumps_text, (self.rect.x + 100,
                                                              self.rect.y + 290))
                self.game.screen.blit(self.total_attempts_text, (self.rect.x + 100,
                                                                 self.rect.y + 340))
                self.game.restart.rect.y += 25
                self.game.menu.rect.y += 25
            else:
                self.game.move_table = False
                self.game.win_table_show = True
