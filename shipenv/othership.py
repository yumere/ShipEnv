import pygame
from pygame import Surface, Rect


class OtherShip(object):
    def __init__(self, start_angle: int, velocity: int = 1, scale: int = 10, center=(), screen_size=()):
        super(OtherShip, self).__init__()
        self.start_angle = start_angle
        self.velocity = velocity
        self.origin_center = center
        self.screen_size = screen_size
        self.img: Surface = pygame.image.load("assets/other_ship_{}.png".format(start_angle))
        self.ship_size = [i // scale for i in self.img.get_size()]
        self.img: Surface = pygame.transform.scale(self.img, self.ship_size)

        self.rect: Rect = self.img.get_rect(center=center)

    def move(self):
        if self.start_angle == 0:
            self.rect.centery -= self.velocity
        elif self.start_angle == 45:
            self.rect.centerx -= self.velocity
            self.rect.centery -= self.velocity
        elif self.start_angle == 90:
            self.rect.centerx -= self.velocity
        elif self.start_angle == 135:
            self.rect.centerx -= self.velocity
            self.rect.centery += self.velocity
        elif self.start_angle == 180:
            self.rect.centery += self.velocity
        elif self.start_angle == 225:
            self.rect.centerx += self.velocity
            self.rect.centery += self.velocity
        elif self.start_angle == 270:
            self.rect.centerx += self.velocity
        elif self.start_angle == 315:
            self.rect.centerx += self.velocity
            self.rect.centery -= self.velocity

        # TODO: if the ship move out screen, move inverse direction
        if self._check_out():
            self.reset()

    def _check_out(self):
        if self.rect.centerx - self.ship_size[0] // 2 < 0:
            return True
        elif self.rect.centerx + self.ship_size[0] // 2 > self.screen_size[0]:
            return True
        if self.rect.centery - self.ship_size[1] // 2 < 0:
            return True
        elif self.rect.centery + self.ship_size[1] // 2 > self.screen_size[1]:
            return True
        return False

    def reset(self):
        self.rect.center = self.origin_center