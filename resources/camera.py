from settings import *


class Camera:
    def __init__(self, game):
        self.game = game
        self.size = (width, height)
        self.offset = 0

    def update(self):
        if self.game.player.rect.centerx > self.size[0] // 2 - 100:
            self.offset = (self.game.player.rect.centerx - self.size[0] // 2 + 100) / 1
            self.game.player.rect.centerx -= self.offset
            self.game.bx -= self.offset // 4
            self.game.win_coords = (self.game.win_coords[0] - self.offset, self.game.win_coords[1])
            self.game.attempt.x -= self.offset

            for x in self.game.blocks.sprites():
                x.update(-self.offset)

            if self.game.bx < -1900:
                self.game.bx = -100
