import pygame as pg
import os
import math
from constants import *
from game_func import *
from bullet import*

pg.init()


class player(object):
    vel_x = 0
    vel_y = 0
    ply_img = pg.transform.scale2x(move_down[0])
    dir = 'down'
    stop = True
    allow = True
    walk_cnt = 0
    dth_cnt = 0
    sprint = False
    dash = False
    bounce = wall_bon
    timer = 0
    stun = False
    s_dur = w_stun
    coll = (False, 0, 0)
    b_tim = [0, 8]
    d_tim = [0, 25]
    f_tim = [0, 40]
    bull_type = blue_fire
    bull_icon = blue_fire
    bull_trvl = 0
    bull_anm = 1
    bull_pen = False
    state = "move"
    n_bull = 0
    eng = 0
    bull_eng = 0

    def __init__(self, x, y, keys):
        self.x = x
        self.y = y
        self.keys = keys

    def move(self):

        global shake
        for i in range(abs(math.ceil(self.vel_x))):
            if self.x + 16 < offset[0] or self.x + 16 + 32 > width - offset[2]:
                wall_hit_sound.play()
                pg.display.update()
                if self.x + 16 < offset[0]:
                    self.coll = (True, offset[0], self.y+char_height/2)
                    self.x += self.bounce
                else:
                    self.coll = (
                        True, width - offset[2] - 20, self.y+char_height/2)
                    self.x -= self.bounce
                self.stop = True
                self.dash = False
                self.allow = False
                self.stun = True
                self.timer = self.s_dur
                self.vel_x = 0
                break
            else:
                self.x += sign(self.vel_x)

        for i in range(abs(math.ceil(self.vel_y))):
            if self.y + 16 < offset[1] or self.y + 16 + 35 > height - offset[3]:
                wall_hit_sound.play()
                if self.y + 16 < offset[1]:
                    self.coll = (True, self.x+char_width/2-10, offset[1])
                    self.y += self.bounce
                else:
                    self.coll = (True, self.x+char_width/2 -
                                 10, height - offset[3] - 20)
                    self.y -= self.bounce
                self.stop = True
                self.dash = False
                self.allow = False
                self.stun = True
                self.timer = self.s_dur
                self.vel_y = 0
                break
            else:
                self.y += sign(self.vel_y)

        if abs(self.vel_x) <= max_vel and not self.stop:
            self.vel_x += acc*sign(self.vel_x)

        if abs(self.vel_y) <= max_vel and not self.stop:
            self.vel_y += acc*sign(self.vel_y)

        if self.sprint and self.vel_x != 0:
            self.vel_x = sprnt*self.vel_x/(abs(self.vel_x))
        if self.sprint and self.vel_y != 0:
            self.vel_y = sprnt*self.vel_y/(abs(self.vel_y))

        if self.stop or self.dash:
            if self.vel_x != 0:
                if sign(self.vel_x) == sign(round(self.vel_x - d_acc*sign(self.vel_x))):
                    self.vel_x = round(self.vel_x - d_acc*sign(self.vel_x))
                else:
                    self.vel_x = 0
            if self.vel_y != 0:
                if sign(self.vel_y) == sign(round(self.vel_y - d_acc*sign(self.vel_y))):
                    self.vel_y = round(self.vel_y - d_acc*sign(self.vel_y))
                else:
                    self.vel_y = 0

        if self.vel_x == 0 and self.vel_y == 0 and not self.stun:
            self.allow = True
            self.dash = False

        if self.timer > 0:
            if self.f_tim[0] == 0:
                if self.dir == 'up' or self.dir == 'down':
                    self.y += (-1)**(self.timer % 2)
                if self.dir == 'left' or self.dir == 'right':
                    self.x += (-1)**(self.timer % 2)
            self.timer -= 1
        else:
            self.stun = False

        if self.sprint:
            sprint_sound.play()

    def get_movements(self):
        keys = pg.key.get_pressed()

        if keys[self.keys[0]] and self.allow and self.d_tim[0] == 0:
            dash_sound.play()
            self.d_tim[0] += 1
            if self.dir == 'up' and self.vel_y == 0:
                self.vel_y = -max_vel*1.5
            elif self.dir == 'down' and self.vel_y == 0:
                self.vel_y = max_vel*1.5
            elif self.dir == 'left' and self.vel_x == 0:
                self.vel_x = -max_vel*1.5
            elif self.dir == 'right' and self.vel_x == 0:
                self.vel_x = max_vel*1.5

            self.vel_x *= dash
            self.vel_y *= dash
            self.dash = True
            self.allow = False

        if keys[self.keys[1]] and self.allow:
            self.sprint = True
            self.bounce = wall_bon*2
            self.s_dur = w_stun*2
        else:

            if self.dir == 'up' and abs(self.vel_y) > max_vel and not self.dash:
                self.vel_y = -max_vel
            elif self.dir == 'down' and abs(self.vel_y) > max_vel and not self.dash:
                self.vel_y = max_vel
            elif self.dir == 'left' and abs(self.vel_x) > max_vel and not self.dash:
                self.vel_x = -max_vel
            elif self.dir == 'right' and abs(self.vel_x) > max_vel and not self.dash:
                self.vel_x = max_vel

            self.sprint = False
            self.bounce = wall_bon
            self.s_dur = w_stun

        if keys[self.keys[3]] and self.allow:
            if self.dir != 'up' or self.stop:
                self.vel_x = 0
                self.vel_y = -int_vel
            self.dir = 'up'
            self.stop = False

        elif keys[self.keys[4]] and self.allow:
            if self.dir != 'down' or self.stop:
                self.vel_x = 0
                self.vel_y = int_vel
            self.dir = 'down'
            self.stop = False

        elif keys[self.keys[5]] and self.allow:
            if self.dir != 'left' or self.stop:
                self.vel_x = -int_vel
                self.vel_y = 0
            self.dir = 'left'
            self.stop = False

        elif keys[self.keys[6]] and self.allow:
            if self.dir != 'right' or self.stop:
                self.vel_x = int_vel
                self.vel_y = 0
            self.dir = 'right'
            self.stop = False
        else:
            self.stop = True
            self.sprint = False
            self.walk_cnt = 0

        if keys[self.keys[2]] and self.b_tim[0] == 0 and self.n_bull > 0 and self.allow:
            if self.bull_type == spark:
                spark_sound.play()
                spark2_sound.play()
                hit_sound.play()
            if self.bull_type == blast:
                blast_sound.play()
                blast2_sound.play()
                hit_sound.play()
            fire_sound.play()

            if self.eng > 0:
                self.eng -= self.bull_eng

            if self.eng < 0:
                self.eng = 0
                self.vel_x = 0
                self.vel_y = 0
                self.stop = True
                self.dash = False
                self.allow = False
                self.stun = True
                self.timer = self.f_tim[1]
                self.f_tim[0] = 1
                self.vel_y = 0

            self.n_bull -= 1
            self.b_tim[0] += 1
            if self.dir == 'up':
                bull.append(bullet(self.x-self.bull_type[0].get_width()//2+char_width//2,
                                   self.y+15, self.bull_type, self.dir, self.bull_trvl, self.bull_anm, self.bull_pen))
            elif self.dir == 'down':
                bull.append(bullet(self.x-self.bull_type[0].get_width()//2+char_width//2,
                                   self.y+20, self.bull_type, self.dir, self.bull_trvl, self.bull_anm, self.bull_pen))
            elif self.dir == 'left':
                bull.append(bullet(self.x+18, self.y-self.bull_type[0].get_width()//2 +
                                   char_height//2, self.bull_type, self.dir, self.bull_trvl, self.bull_anm, self.bull_pen))
            elif self.dir == 'right':
                bull.append(bullet(self.x+18, self.y-self.bull_type[0].get_width()//2 +
                                   char_height//2, self.bull_type, self.dir, self.bull_trvl, self.bull_anm, self.bull_pen))

    def cooldown(self):
        if self.b_tim[0] > 0:
            self.b_tim[0] += 1
        if self.b_tim[0] == self.b_tim[1]:
            self.b_tim[0] = 0

        if self.d_tim[0] > 0:
            self.d_tim[0] += 1
        if self.d_tim[0] == self.d_tim[1]:
            self.d_tim[0] = 0

        if self.f_tim[0] > 0:
            self.f_tim[0] += 1
        if self.f_tim[0] == self.f_tim[1]:
            self.f_tim[0] = 0

    def draw(self):
        if self.dir == 'up':
            if self.dash:
                self.ply_img = pg.transform.scale2x(dsh[0])
            else:
                self.ply_img = pg.transform.scale2x(move_up[self.walk_cnt])
        elif self.dir == 'down':
            if self.dash:
                self.ply_img = pg.transform.scale2x(dsh[2])
            else:
                self.ply_img = pg.transform.scale2x(move_down[self.walk_cnt])
        elif self.dir == 'left':
            if self.dash:
                self.ply_img = pg.transform.scale2x(dsh[3])
            else:
                self.ply_img = pg.transform.scale2x(move_left[self.walk_cnt])
        elif self.dir == 'right':
            if self.dash:
                self.ply_img = pg.transform.scale2x(dsh[1])
            else:
                self.ply_img = pg.transform.scale2x(move_right[self.walk_cnt])

        if (abs(self.vel_x) == 0 and abs(self.vel_y) < max_vel+acc) or (abs(self.vel_x) < max_vel+acc and abs(self.vel_y) == 0):
            spd = 0
        elif (abs(self.vel_x) == 0 and abs(self.vel_y) == max_vel+acc) or (abs(self.vel_x) == max_vel+acc and abs(self.vel_y) == 0):
            spd = 0
        elif (abs(self.vel_x) == 0 and abs(self.vel_y) > max_vel+acc) or (abs(self.vel_x) >= max_vel+acc and abs(self.vel_y) == 0):
            spd = 1

        if self.dash:
            if self.dir == 'up':
                win.blit(pg.transform.rotate(walk_eff[3], 90),
                         (self.x+23, self.y+53))
            elif self.dir == 'down':
                win.blit(pg.transform.rotate(
                    walk_eff[3], -90), (self.x+23, self.y+5))
            elif self.dir == 'left':
                win.blit(pg.transform.flip(
                    walk_eff[3], True, False), (self.x+38, self.y+32))
            elif self.dir == 'right':
                win.blit(walk_eff[3], (self.x+12, self.y+32))

        elif self.vel_x != 0 or self.vel_y != 0:
            if self.dir == 'up':
                win.blit(pg.transform.rotate(walk_eff[spd], 90),
                         (self.x+27, self.y+53))
            elif self.dir == 'down':
                win.blit(pg.transform.rotate(
                    walk_eff[spd], -90), (self.x+27, self.y+20))
            elif self.dir == 'left':
                win.blit(pg.transform.flip(
                    walk_eff[spd], True, False), (self.x+37, self.y+45))
            elif self.dir == 'right':
                win.blit(walk_eff[spd], (self.x+18, self.y+45))

        global i_cnt

        if self.d_tim[0] != 0:
            fct = 5
            col = tuple((
                blue[0]+int((red[0]-blue[0])/self.d_tim[1]*self.d_tim[0]//fct),
                blue[1]+int((red[1]-blue[1])/self.d_tim[1]*self.d_tim[0]//fct),
                blue[2]+int((red[2]-blue[2])/self.d_tim[1]*self.d_tim[0]//fct)
            ))
            dcol = tuple((
                dblue[0]+int((dred[0]-dblue[0])/self.d_tim[1]
                             * self.d_tim[0]//fct),
                dblue[1]+int((dred[1]-dblue[1])/self.d_tim[1]
                             * self.d_tim[0]//fct),
                dblue[2]+int((dred[2]-dblue[2])/self.d_tim[1]
                             * self.d_tim[0]//fct)
            ))
            self.ply_img = color_chng(self.ply_img, red, col)
            self.ply_img = color_chng(self.ply_img, dred, dcol)

        if self.f_tim[0] != 0:
            fct = 3

            col = tuple((
                gry[0]+int((red[0]-gry[0])/self.f_tim[1]*self.f_tim[0]//fct),
                gry[1]+int((red[1]-gry[1])/self.f_tim[1]*self.f_tim[0]//fct),
                gry[2]+int((red[2]-gry[2])/self.f_tim[1]*self.f_tim[0]//fct)
            ))
            dcol = tuple((
                dgry[0]+int((dred[0]-dgry[0])/self.f_tim[1]
                            * self.f_tim[0]//fct),
                dgry[1]+int((dred[1]-dgry[1])/self.f_tim[1]
                            * self.f_tim[0]//fct),
                dgry[2]+int((dred[2]-dgry[2])/self.f_tim[1]
                            * self.f_tim[0]//fct)
            ))

            self.ply_img = color_chng(self.ply_img, red, col)
            self.ply_img = color_chng(self.ply_img, dred, dcol)

        if self.vel_x == 0 and self.vel_y == 0 and self.timer == 0:
            if idle[i_cnt] == 0:
                win.blit(self.ply_img, (self.x, self.y))
                i_cnt += 1
            elif idle[i_cnt] == 1:
                win.blit(pg.transform.scale(self.ply_img,
                                            (char_width, char_height - 2)), (self.x, self.y+1))
                i_cnt += 1
            elif idle[i_cnt] == 2:
                win.blit(pg.transform.scale(self.ply_img,
                                            (char_width, char_height - 4)), (self.x, self.y+3))
                i_cnt += 1
            if i_cnt == len(idle):
                i_cnt = 0

        else:
            win.blit(self.ply_img, (self.x, self.y))

        if self.coll[0]:
            win.blit(wall_eff[1], (self.coll[1], self.coll[2]))
            self.coll = (False, 0, 0)

        if self.walk_cnt == 3:
            self.walk_cnt = 0
        else:
            self.walk_cnt += 1

    def death(self, end):
        self.allow = False
        win.blit(shock[int(self.dth_cnt)], (self.x+32 -
                                            shock[0].get_width()/2, self.y+32-shock[0].get_width()/2))
        self.dth_cnt += 1

        if self.dth_cnt >= len(shock) and end == "end":
            pg.mixer.music.pause()
            gameover_sound.play()
            self.state = end
        if self.dth_cnt >= len(shock)-5 and end == "spawn":
            pg.mixer.music.pause()
            self.state = end

    def spawn(self):
        self.dth_cnt -= 1
        if self.dth_cnt < 0:
            self.dth_cnt = 0

        self.allow = False
        win.blit(shock[int(self.dth_cnt)], (self.x+32 -
                                            shock[0].get_width()/2, self.y+32-shock[0].get_width()/2))

        if self.dth_cnt == 0:
            self.timer = 0
            pg.mixer.music.play(-1)
            self.state = "move"

    def chng_bull(self, bull_icon, bullet, bull_trvl, pen, n_bull, anm, bull_eng):
        self.bull_icon = bull_icon
        self.bull_type = bullet
        self.bull_trvl = bull_trvl
        self.bull_anm = anm
        self.bull_pen = pen
        self.n_bull = n_bull
        self.bull_eng = bull_eng
