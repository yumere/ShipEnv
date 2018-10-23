# TODO: Obstacles will be generated randomly
# TODO: Other ships must be added as dynamic obstacles

import math
import sys

import numpy as np
import pygame
from pygame import Rect

from shipenv.action import Action
from shipenv.othership import OtherShip
from shipenv.ship import Ship

# Color constants
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)

# State constants
STATE_COLLISION = 0
STATE_IN_DESTINATION = 1
STATE_IN_SAILING = 3


class ShipEnv(object):
    def __init__(self, screen_size=(), fps=30):
        super(ShipEnv, self).__init__()
        self.screen_size = screen_size
        self.fps = fps
        self.action_space = Action()

        self.other_ships = []
        self.static_obstacles = []
        pygame.init()

        self.screen: pygame.Surface = pygame.display.set_mode(self.screen_size)
        self._create_other_ships()
        self._create_obstacles()

        # TODO: destination point need to be placed randomly
        self.dest = Rect(self.screen_size[0] - 20 - 10, 20, 20, 20)
        self.dest_center = self.dest.center
        self.my_ship = Ship(velocity=2, scale=10, center=(self.screen_size[0] // 2, self.screen_size[1] // 2), screen_size=self.screen_size)

        self.old_dist = math.sqrt(((np.array(self.dest_center) - np.array(self.my_ship.rect.center)) ** 2).sum())
        self.dist = self.old_dist

        self.clock = pygame.time.Clock()

        class Monitor(object):
            def start(self, gym_dir):
                pass

        self.monitor = Monitor()

    def step(self, action):
        """

        :param action: 0: stop, 1: start, 2: left 45 rotate, 3: right 45 rotate
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.clock.tick(self.fps)

        # TODO: Make action space to sample
        if action == 0:
            pass
        elif action == 1:
            self.my_ship.move()
        elif action == 2:
            self.my_ship.rotate(direction='left')
        elif action == 3:
            self.my_ship.rotate(direction='right')
        else:
            pass

        for other_ship in self.other_ships:
            other_ship.move()

        self._handle_collisions()
        if self.state == STATE_IN_DESTINATION:
            reward = 1.
        elif self.state == STATE_COLLISION:
            reward = -1.
        elif self.state == STATE_IN_SAILING:
            self.dist = math.sqrt(((np.array(self.dest_center) - np.array(self.my_ship.rect.center)) ** 2).sum())
            if self.old_dist > self.dist:
                reward = 0.001
            else:
                reward = -0.001
            self.old_dist = self.dist

        self._update_screen()
        observation = pygame.surfarray.array3d(self.screen)

        # State is either PLAYING OR GAME OVER
        return observation, reward, True if self.state == STATE_IN_DESTINATION or self.state == STATE_COLLISION else False, {}

    def reset(self):
        self.state = STATE_IN_SAILING

        for other_ship in self.other_ships:
            other_ship.reset()
        self.my_ship.reset()

        self._update_screen()
        observation = pygame.surfarray.array3d(self.screen)

        return observation, 0, False, {}

    def _handle_collisions(self):
        for obstacle in self.static_obstacles:
            # whether occur collision between my ship and static obstacles
            if self.my_ship.rect.colliderect(obstacle):
                self.state = STATE_COLLISION
                return

            # Whether occur collision between other and static obstacles
            for other_ship in self.other_ships:
                if other_ship.rect.colliderect(obstacle):
                    other_ship.reset()

        # Whether occur collision between my ship and other ships
        for other_ship in self.other_ships:
            if other_ship.rect.colliderect(self.my_ship.rect):
                self.state = STATE_COLLISION
                return

        # TODO: handle the collisions between other ships
        # for i, other_ship1 in enumerate(self.other_ships):
        #     for j, other_ship2 in enumerate(self.other_ships[i:]):
        #         pass

        # If the ship arrive the destination
        if self.my_ship.rect.colliderect(self.dest):
            self.state = STATE_IN_DESTINATION

    def _update_screen(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, RED, self.dest)
        self._draw_obstacles()
        self._draw_other_ships()
        self.screen.blit(self.my_ship.img, self.my_ship.rect)
        pygame.display.flip()

    def _create_other_ships(self):
        self.other_ships.append(OtherShip(start_angle=45, velocity=1, scale=10, center=(245, 280), screen_size=self.screen_size))
        self.other_ships.append(OtherShip(start_angle=270, velocity=1, scale=10, center=(30, 100), screen_size=self.screen_size))

    def _create_obstacles(self):
        self.static_obstacles.append(Rect(20, 20, 10, 40))
        self.static_obstacles.append(Rect(100, 60, 25, 5))
        self.static_obstacles.append(Rect(160, 30, 20, 5))
        self.static_obstacles.append(Rect(80, 130, 30, 5))
        self.static_obstacles.append(Rect(230, 180, 10, 30))
        self.static_obstacles.append(Rect(250, 80, 10, 20))
        self.static_obstacles.append(Rect(30, 250, 30, 30))
        self.static_obstacles.append(Rect(150, 250, 30, 5))

    def _draw_obstacles(self):
        for obstacle in self.static_obstacles:
            pygame.draw.rect(self.screen, GRAY, obstacle)

    def _draw_other_ships(self):
        for other_ship in self.other_ships:
            self.screen.blit(other_ship.img, other_ship.rect)
