import pygame as pg
from constants import *


# to return the sign of value

def sign(x):
    try:
        return round(x/abs(x))
    except ZeroDivisionError:
        return 0

# to check collision


def collide(img, img1, x, y, x1, y1):
    player_mask = pg.mask.from_surface(img)
    obj_mask = pg.mask.from_surface(img1)

    offset = (int(x1-x), int(y1-round(y)))

    col_point = player_mask.overlap(obj_mask, offset)

    if col_point:
        return True
    return False

# shake screen


def distance(cord1, cord2):
    return ((cord1[0]-cord2[0])**2+(cord1[1]-cord2[1])**2)**0.5


def color_chng(img, col1, col2):

    image_pixel_array = pg.PixelArray(img.convert_alpha())
    image_pixel_array.replace(col1, col2)
    img = pg.PixelArray.make_surface(image_pixel_array)

    return img


def heart(life):

    for i in range(4):
        win.blit(pg.transform.scale(health[0], (16, 16)), (width-10-i*20, 5))

    for i in range(life):
        win.blit(pg.transform.scale(health[1], (16, 16)), (width-10-i*20, 5))


class button():
    def __init__(self, x, y, img, width, height, mg=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.mg = mg

    def draw(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            win.blit(pg.transform.scale(self.img, (self.width+self.mg,
                                                   self.height+self.mg)), (self.x - self.mg/2, self.y - self.mg/2))
        else:
            win.blit(self.img, (self.x, self.y))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class powerup():

    cnt = 0
    time_cnt = 0

    def __init__(self, x, y, bull_prop):
        self.x = x
        self.y = y
        self.time = 200
        self.pwr_up = bull_prop[0]
        self.fct = bull_prop[1]
        self.bullet = bull_prop[2]
        self.bull_trvl = bull_prop[3]
        self.pen = bull_prop[4]
        self.anm = bull_prop[5]
        self.n_bull = bull_prop[6]
        self.bull_eng = bull_prop[7]

    def draw(self):
        win.blit(self.pwr_up[self.cnt//self.fct], (self.x, self.y))
        self.cnt += 1
        self.time_cnt += 1
        if self.cnt == len(self.pwr_up)*self.fct:
            self.cnt = 0

    def pickup(self, ply):
        if collide(ply.ply_img, self.pwr_up[self.cnt//self.fct], ply.x, ply.y, self.x, self.y):
            ply.chng_bull(self.pwr_up, self.bullet, self.bull_trvl,
                          self.pen, self.n_bull, self.anm, self.bull_eng)
            return True
        return False


class time_obj():

    def __init__(self, x, y, img, time):
        self.x = x
        self.y = y
        self.time = time
        self.img = img
        self.fct = int(self.time//10//4)

    def draw(self):
        img = self.img
        if self.time//10 <= self.fct:
            col = tuple((
                green[0]+int((grnd[0]-green[0])/self.fct *
                             (self.fct-(self.time//10))),
                green[1]+int((grnd[1]-green[1])/self.fct *
                             (self.fct-(self.time//10))),
                green[2]+int((grnd[2]-green[2])/self.fct *
                             (self.fct-(self.time//10)))
            ))
            img = color_chng(self.img, green, col)
        win.blit(img, (self.x, self.y))
        if self.time > 0:
            self.time -= 1


def num_print(win, score, x, y, col=(255, 255, 255), b_col=(0, 0, 0)):
    number = []
    if score == 0:
        number.append(0)
    else:
        while score > 0:
            number.append(score % 10)
            score //= 10
    i = (len(number)-1)
    while i >= 0:
        img = color_chng(digit[number[i]], (255, 255, 255), col)
        img = color_chng(img, (20, 24, 28), b_col)
        win.blit(img, (x, y))
        x += 27
        i -= 1
    return x


def mute_sound(mute):
    if mute:
        vlm = 0
    else:
        vlm = 1
    hit_sound.set_volume(vlm)
    fire_sound.set_volume(vlm)
    spark_sound.set_volume(vlm)
    spark2_sound.set_volume(vlm)
    blast_sound.set_volume(vlm)
    blast2_sound.set_volume(vlm)
    dash_sound.set_volume(vlm)
    wall_hit_sound.set_volume(vlm)
    sprint_sound.set_volume(vlm)
    death_sound.set_volume(vlm)
    death2_sound.set_volume(vlm)
    gameover_sound.set_volume(vlm)
    select_sound.set_volume(vlm)
    start_sound.set_volume(vlm)


def mute_music(mute):
    if mute:
        vlm = 0
    else:
        vlm = 1
    pg.mixer.music.set_volume(vlm)
