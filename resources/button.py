import pygame

from settings import font


class Button(pygame.Rect):
    def __init__(self, game, width, height, x, y, func, font=font):
        self.font = font
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.game = game
        self.func = func
        super().__init__((self.x, self.y, self.width, self.height))

    def draw(self):
        pygame.draw.rect(self.game.screen, "green", (self.x, self.y, self.width, self.height))


class Button_Sprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y, func, image, resizemode=1, current=False):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.game = game
        self.func = func
        self.current = current
        if resizemode == 1:
            self.image = pygame.transform.scale(pygame.image.load(f"assets/{image}").convert_alpha(), (150, 150))
        else:
            self.image = pygame.transform.scale(pygame.image.load(f"assets/{image}").convert_alpha(), (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def show(self):
        self.game.screen.blit(self.image, (self.x, self.y))


class Button_Sprite_skin(pygame.sprite.Sprite):
    def __init__(self, game, x, y, func, image, numero, resizemode=1, current=False):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.game = game
        self.func = func
        self.numero = numero
        self.image_name = image
        self.current = current
        if resizemode == 1:
            self.image = pygame.transform.scale(pygame.image.load(f"assets/{image}").convert_alpha(), (150, 150))
        else:
            self.image = pygame.transform.scale(pygame.image.load(f"assets/{image}").convert_alpha(), (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def show(self):
        self.game.screen.blit(self.image, (self.x, self.y))

    def change_image(self, new):
        self.image = pygame.transform.scale(pygame.image.load(f"assets/{new}").convert_alpha(), (150, 150))
