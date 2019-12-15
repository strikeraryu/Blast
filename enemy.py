import pygame as pg
import os
import math
import random
from constants import *
from game_func import *
from bullet import *

pg.init()


class enemy(object):

    wlk_cnt = 0
    state = "spawn"

    def __init__(self, enm_s, enm_f, enm_b, enm_spawn, enm_die, enm_dieb, vel, x, y, width, height):
        self.enm_s = enm_s
        self.enm_b = enm_b
        self.enm_f = enm_f
        self.enm_spawn = enm_spawn
        self.enm_die = enm_die
        self.enm_dieb = enm_die
        self.img = enm_f[0]
        self.vel = vel
        self.dir = "down"
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        if self.state == "move":
            fct = 2

            if self.dir == "down":
                self.img = self.enm_f[self.wlk_cnt//fct]
            if self.dir == "up":
                self.img = self.enm_b[self.wlk_cnt//fct]
            if self.dir == "left":
                self.img = self.enm_s[self.wlk_cnt//fct]
            if self.dir == "right":
                self.img = pg.transform.flip(
                    self.enm_s[self.wlk_cnt//fct], True, False)
            self.img = pg.transform.scale(self.img, (self.width, self.height))
            win.blit(self.img, (self.x, self.y))

            self.wlk_cnt += 1

            if self.wlk_cnt >= len(self.enm_f)*fct:
                self.wlk_cnt = 0

        elif self.state == "spawn":
            fct = 2

            win.blit(pg.transform.scale(
                self.enm_spawn[self.wlk_cnt//fct], (self.width, self.height)), (self.x, self.y))

            self.wlk_cnt += 1
            if self.wlk_cnt >= len(self.enm_spawn)*fct:
                self.state = "move"
                self.wlk_cnt = 0

        elif self.state == "die":
            fct = 2

            if self.dir == "up":
                win.blit(pg.transform.scale(
                    self.enm_dieb[self.wlk_cnt//fct], (self.width, self.height)), (self.x, self.y))
            else:
                win.blit(pg.transform.scale(
                    self.enm_die[self.wlk_cnt//fct], (self.width, self.height)), (self.x, self.y))

            self.wlk_cnt += 1
            if self.wlk_cnt >= len(self.enm_die)*fct:
                self.state = "end"
                self.wlk_cnt = 0

    def move(self, ply_x, ply_y):

        if self.state == "move":
            dist = distance((self.x, self.y), (ply_x, ply_y))
            dist_r = distance((self.x+self.vel, self.y), (ply_x, ply_y))
            dist_l = distance((self.x-self.vel, self.y), (ply_x, ply_y))
            dist_d = distance((self.x, self.y+self.vel), (ply_x, ply_y))
            dist_u = distance((self.x, self.y-self.vel), (ply_x, ply_y))
            dist_rd = distance(
                (self.x+self.vel/2, self.y+self.vel/2), (ply_x, ply_y))
            dist_ld = distance(
                (self.x-self.vel/2, self.y+self.vel/2), (ply_x, ply_y))
            dist_ru = distance(
                (self.x+self.vel/2, self.y-self.vel/2), (ply_x, ply_y))
            dist_lu = distance(
                (self.x-self.vel/2, self.y-self.vel/2), (ply_x, ply_y))

            if abs(abs(self.y-ply_y) - abs(self.x-ply_x)) <= 2:
                if dist_rd < dist:
                    self.x += self.vel/2
                    self.y += self.vel/2
                    self.dir = "right"
                elif dist_ld < dist:
                    self.x -= self.vel/2
                    self.y += self.vel/2
                    self.dir = "left"
                elif dist_ru < dist:
                    self.x += self.vel/2
                    self.y -= self.vel/2
                    self.dir = "right"
                elif dist_lu < dist:
                    self.x -= self.vel/2
                    self.y -= self.vel/2
                    self.dir = "left"
            else:
                if dist_r < dist and dist_r <= dist_u and dist_r <= dist_d:
                    self.x += self.vel
                    self.dir = "right"
                elif dist_l < dist and dist_l <= dist_u and dist_l <= dist_d:
                    self.x -= self.vel
                    self.dir = "left"
                elif dist_d < dist and dist_d <= dist_l and dist_d <= dist_r:
                    self.y += self.vel
                    self.dir = "down"
                elif dist_u < dist and dist_u <= dist_l and dist_u <= dist_r:
                    self.y -= self.vel
                    self.dir = "up"

    def kill(self, ply_img, ply_x, ply_y):
        if collide(self.img, ply_img, self.x, self.y, ply_x, ply_y) and self.state == "move":
            return True
        return False

    def die(self, bul_img, bul_x, bul_y, play=True):
        if collide(self.img, bul_img, self.x, self.y, bul_x, bul_y):
            self.state = "die"
            if play:
                hit_sound.play()
            return True
        return False


def gen_slm(n, ply_x, ply_y):
    enm_lst = []
    for i in range(n):
        fct = 30
        chk = False
        while not chk:
            tmp_x = random.randrange(offset[0] + fct, width-fct - offset[2])
            tmp_y = random.randrange(fct + offset[1], height-fct-offset[3])
            if distance((tmp_x, tmp_y), (ply_x, ply_y)) > fct+30:
                chk = True
        gen_enm = enemy(slm_s, slm_f, slm_b, slm_spawn, slm_die, slm_dieb,
                        slm_vel, tmp_x, tmp_y, slm_size, slm_size)
        enm_lst.append(gen_enm)
    return enm_lst
