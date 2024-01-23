import pygame


class Button_Sprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y, func, image, resizemode=1, current=False, level=1):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.game = game
        self.func = func
        self.level = level
        self.current = current

        if resizemode == 1:
            self.image = pygame.transform.scale(pygame.image.load(f"assets/{image}").convert_alpha(), (150, 150))
        elif resizemode == 2:
            self.image = pygame.image.load(f"assets/{image}").convert_alpha()
        else:
            self.image = pygame.transform.scale(pygame.image.load(f"assets/{image}").convert_alpha(), (60, 60))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def show(self):
        self.game.screen.blit(self.image, self.rect.topleft)

    def change_image(self, new):
        self.image = pygame.transform.scale(pygame.image.load(f"assets/{new}").convert_alpha(), (150, 150))


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

    def check_current(self, num):
        if self.numero == num:
            self.current = True

    def show(self):
        self.game.screen.blit(self.image, (self.x, self.y))

    def change_image(self, new):
        self.image = pygame.transform.scale(pygame.image.load(f"assets/{new}").convert_alpha(), (150, 150))


class Button_Sprite_Win(pygame.sprite.Sprite):
    def __init__(self, game, x, y, func, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.game = game
        self.func = func
        self.image = pygame.transform.scale(pygame.image.load(f"assets/{image}").convert_alpha(), (150, 150))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def show(self):
        self.game.screen.blit(self.image, self.rect.topleft)
