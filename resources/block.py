from settings import *


class Block(pygame.sprite.Sprite):
    def __init__(self, game, position, bid):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.type = bid
        if bid not in range(97, 100) and bid != 3:
            self.image = pygame.transform.scale(pygame.image.load(blocks_bid.get(bid)).convert_alpha(), (70, 70))
        else:
            self.image = pygame.image.load(blocks_bid.get(bid)).convert_alpha()
        self.rect = self.image.get_rect()
        self.add(self.game.blocks)
        self.pos = position
        self.rect.topleft = self.pos
        self.hitbox = pygame.mask.from_surface(self.image)
        self.hitbox_surface = self.hitbox.to_surface()

    def update(self, offset):
        self.rect.x += offset
        if 0 < self.rect.right < 50 and 200 < self.game.player.rect.x:
            self.rect.top -= 20
        if self.rect.right < 0:
            self.kill()
