import random

from resources.particles import Particle
from resources.particle_cube import Particle_Cube
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.jumps = 0
        self.len = 0
        self.game = game
        self.orig_image = pygame.transform.scale(pygame.image.load("assets/skin1.png").convert_alpha(), (70, 70))
        self.speedx = 10
        self.is_jumping = False
        self.falling = False
        self.pos = (0, 0)
        self.counter = GRAVITY
        self.angle = 0
        self.add(self.game.players)
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 670
        self.hitbox = pygame.mask.from_surface(self.image)
        self.hitbox_surface = self.hitbox.to_surface()
        self.last = 0
        self.particle_enable = True
        self.death_event = pygame.USEREVENT + 6
        self.died = False
        self.music_offed = False

    def check_angle(self):
        result = []
        sorted_angles = sorted(angles)
        for i in range(len(sorted_angles) - 1):
            if sorted_angles[i] < self.angle < sorted_angles[i + 1]:
                result.append(sorted_angles[i])
                result.append(sorted_angles[i + 1])
        temp = 999
        index = 0
        result.sort()
        for i, angle in enumerate(result):
            # print(abs(angle) - abs(self.angle))
            if abs(angle) - abs(self.angle) < temp:
                temp = abs(angle) - abs(self.angle)
                if 18 > angle - self.angle > 0:
                    index = i
                    break
            # elif abs(angle) - abs(self.angle) > temp:
            #     temp = abs(angle) - abs(self.angle)
            #     index = i
        try:
            # print("sub1", result[index], f"self.angle: {self.angle}")
            # print(f"sub: {abs(result[index]) - abs(self.angle)}")
            if abs(result[index]) - abs(self.angle) < 0:
                sign = '+'
            else:
                sign = '-'
            # print(result)
            # print("+=============func^==========================+")
            return result[index], sign
        except IndexError:
            pass

    @staticmethod
    def ch_angle(angle):
        if angle <= 0:
            if -70 >= angle >= -90 or angle <= -90:
                if -169 >= angle >= -180 or angle <= -180:
                    if angle <= -270:
                        if -360 <= angle <= -270:
                            return -270
                        elif angle <= -360:
                            return 0
                        return -270
                    return -180
                return -90
            return 0

    def gravity(self):
        if self.is_jumping:
            self.angle -= 6
            if self.counter >= -GRAVITY:
                self.rect.y -= self.counter
                self.counter -= 1

                # print("В прыжке", self.angle)
            else:
                feedback = self.check_angle()
                try:
                    if self.angle != feedback[0]:
                        self.angle = eval(f"{self.angle} {feedback[1]} 6")
                except TypeError:
                    pass
                self.is_jumping = False
                self.counter = GRAVITY

                # print("В прыжке2", self.angle)
            self.pos = self.rect.center
            if self.angle == -360:
                self.angle = 0
            self.image = pygame.transform.rotate(self.orig_image, self.angle)
            self.rect = self.image.get_rect(center=self.pos)
        elif self.falling:
            if self.last > 1:
                # print("падаю", self.angle)
                self.angle -= 6
                self.pos = self.rect.center
                if self.angle <= -360:
                    self.angle += 354
                self.image = pygame.transform.rotate(self.orig_image, self.angle)
                self.rect = self.image.get_rect(center=self.pos)
                # print("Градус в конце gцикла падения -", self.angle)
            else:
                # print("коснулся", self.angle, self.counter)
                if self.particle_enable:
                    self.create_particles(self.rect.midbottom)
                self.pos = self.rect.center
                feedback = self.check_angle()
                try:
                    if self.angle != feedback[0]:
                        self.angle = eval(f"{self.angle} {feedback[1]} 6")
                except TypeError:
                    pass
                self.image = pygame.transform.rotate(self.orig_image, self.angle)
                self.rect = self.image.get_rect(center=self.pos)
            self.rect.y += 13

        else:
            if self.particle_enable:
                self.create_particles(self.rect.bottomleft)
            self.pos = self.rect.center
            feedback = self.check_angle()
            try:
                if self.angle != feedback[0]:
                    self.angle = eval(f"{self.angle} {feedback[1]} 6")
            except TypeError:
                pass
            if self.angle <= -360:
                self.angle += 354
            self.image = pygame.transform.rotate(self.orig_image, self.angle)
            self.rect = self.image.get_rect(center=self.pos)
            if self.particle_enable:
                self.create_particles(self.rect.bottomleft)

    def collide(self):
        blocks_hit_list = pygame.sprite.spritecollide(self, self.game.blocks, False)
        self.len = len(blocks_hit_list)
        if self.len == 0:
            self.last += 1
        if len(blocks_hit_list) > 0:
            for block in blocks_hit_list:
                if block.type == 99:
                    pygame.time.set_timer(self.game.pulse_event, 700)
                elif block.type == 98:
                    pygame.time.set_timer(self.game.change_bg_event, 1000)
                elif block.type == 97:
                    pygame.time.set_timer(self.game.win_event, 200)
                else:
                    overlapmask = self.hitbox.overlap_mask(block.hitbox, (
                        block.rect.topleft[0] - self.rect.topleft[0],
                        block.rect.topleft[1] - self.rect.topleft[1]))
                    if (block.rect.bottom > self.rect.top > block.rect.top and overlapmask.count() > 30 and
                            not self.died):
                        self.falling = False
                        self.is_jumping = False
                        self.counter = GRAVITY
                        self.die()
                    elif (block.rect.top - 1 <= self.rect.bottom <= block.rect.bottom and self.falling and
                          block.type not in range(
                            1, 7) and not self.died):  # na bloke stoyat'
                        self.rect.bottom = block.rect.top + 1
                        self.is_jumping = False
                        self.falling = False
                        self.last = 0
                        self.counter = GRAVITY
                    elif overlapmask.count() > 320 and not self.died:
                        self.die()
                    if block.rect.top <= self.rect.top <= block.rect.bottom and not self.died:
                        self.die()
        else:
            self.falling = True
        if self.rect.y > 900 and not self.died:
            self.die()

    def create_particles(self, position):
        particle_count = 1
        pos2 = (position[0] - 12, position[1] - 15)
        numbers = range(-2, 2)
        for _ in range(particle_count):
            Particle(pos2, random.choice(numbers), self.game)

    def death_particle(self):
        particle_count = 10
        pos2 = self.rect.center
        numbers = range(-12, 12)
        for _ in range(particle_count):
            Particle_Cube(pos2, random.choice(numbers), self.game)

    def die(self, mil_sec_death=1250):
        self.died = True
        self.game.attempts += 1
        self.game.progress_add = 0
        pygame.time.set_timer(self.game.pulse_event, 0)
        levels_musics.get(self.game.num_level).stop()
        death.play()
        self.game.players.empty()
        self.game.particles.empty()
        self.speedx = 0
        self.death_particle()
        self.particle_enable = False
        pygame.time.set_timer(self.death_event, mil_sec_death)

    def change_skin(self, skin_id):
        self.orig_image = pygame.transform.scale(pygame.image.load(skins.get(skin_id)).convert_alpha(), (70, 70))

    def update_(self, offset):
        self.gravity()
        self.collide()
        self.hitbox = pygame.mask.from_surface(self.image)
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE] or mouse[0]) and not self.falling:
            self.jumps += 1
            self.is_jumping = True
        self.rect.x += self.speedx
        self.rect.x += offset
