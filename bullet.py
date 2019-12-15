import pygame as pg
from constants import *
from game_func import *

pg.init()


class bullet(object):
    vel_x = 0
    vel_y = 0
    cnt = 0
    trvl_cnt = 0

    def __init__(self, x, y, typ, direction, trvl_dist, anm, pen):
        self.x = x
        self.y = y
        self.anm = anm
        self.type = typ
        self.bull_img = typ[0]
        self.pen = pen
        self.dir = direction
        self.trvl_dist = trvl_dist

    def move(self):

        if self.dir == 'up':
            self.vel_y = -bul_vel
            self.vel_x = 0
        elif self.dir == 'down':
            self.vel_y = bul_vel
            self.vel_x = 0
        elif self.dir == 'left':
            self.vel_x = -bul_vel
            self.vel_y = 0
        elif self.dir == 'right':
            self.vel_x = bul_vel
            self.vel_y = 0

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):

        if self.dir == 'up':
            self.bull_img = pg.transform.flip(
                self.type[self.cnt//self.anm], False, True)
        elif self.dir == 'down':
            self.bull_img = self.type[self.cnt//self.anm]
        elif self.dir == 'left':
            self.bull_img = pg.transform.rotate(
                self.type[self.cnt//self.anm], -90)
        elif self.dir == 'right':
            self.bull_img = pg.transform.rotate(
                self.type[self.cnt//self.anm], 90)
        win.blit(self.bull_img, (self.x, self.y))

        self.cnt += 1
        self.trvl_cnt += 1
        if self.cnt >= len(self.type)*self.anm:
            self.cnt = 0


bull = []
