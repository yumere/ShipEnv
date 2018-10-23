import pygame
from pygame import Surface


class Ship(object):
    def __init__(self, velocity: int=1, scale: int=10, center=(), screen_size=()):
        super(Ship, self).__init__()

        self.start_angle = 0
        self.velocity = velocity
        self.origin_center = center
        self.screen_size = screen_size

        self.origin_img: Surface = pygame.image.load("images/self_ship.png")
        self.ship_size = [i // scale for i in self.origin_img.get_size()]
        self.origin_img: Surface = pygame.transform.scale(self.origin_img, self.ship_size)
        self.img: Surface = pygame.transform.scale(self.origin_img, self.ship_size)

        self.rect = self.img.get_rect()
        self.rect.center = center

        self.angle = 0

    def move(self):
        if self.angle == 45:
            self.rect.centerx -= self.velocity
            self.rect.centery -= self.velocity
        elif self.angle == 90:
            self.rect.centerx -= self.velocity
        elif self.angle == 135:
            self.rect.centerx -= self.velocity
            self.rect.centery += self.velocity
        elif self.angle == 180:
            self.rect.centery += self.velocity
        elif self.angle == 225:
            self.rect.centerx += self.velocity
            self.rect.centery += self.velocity
        elif self.angle == 270:
            self.rect.centerx += self.velocity
        elif self.angle == 315:
            self.rect.centerx += self.velocity
            self.rect.centery -= self.velocity
        elif self.angle == 0 or self.angle == 360:
            self.rect.centery -= self.velocity

        # Can not get out of screen
        if self.rect.centerx - self.ship_size[0] // 2 < 0:
            self.rect.centerx = 0 + self.rect.width // 2
        elif self.rect.centerx + self.ship_size[0] // 2 > self.screen_size[0]:
            self.rect.centerx = self.screen_size[0] - self.ship_size[0] // 2

        if self.rect.centery + self.ship_size[1] // 2 < 0:
            self.rect.centery = 0 + self.ship_size[1] // 2
        elif self.rect.centery + self.ship_size[1] // 2 > self.screen_size[1]:
            self.rect.centery = self.screen_size[1] - self.ship_size[1]

    def rotate(self, direction):
        origin_center = self.rect.center
        self.img = pygame.transform.scale(self.origin_img, self.ship_size)
        if direction == 'left':
            if self.angle == 360:
                self.angle = 0
            self.angle += 45
            self.img = pygame.transform.rotate(self.img, self.angle)
        elif direction == 'right':
            if self.angle == 0:
                self.angle = 360
            self.angle -= 45
            self.img = pygame.transform.rotate(self.img, self.angle)

        self.rect = self.img.get_rect()
        self.rect.center = origin_center

    def reset(self):
        self.rect.center = self.origin_center
