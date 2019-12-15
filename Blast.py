import pygame as pg
import os
import random
import math
from player import *
from constants import *
from bullet import *
from enemy import *


pg.init()

bg_cnt = 0
bull_anm_cnt = 0


def gameboard():
    global bg_cnt
    win.fill((0, 0, 0))
    win.blit(bg[bg_cnt//3], (5, 20))

    bg_cnt += 1
    if bg_cnt == len(bg)*3:
        bg_cnt = 0


def redraw():
    global bull_anm_cnt
    gameboard()

    for i in time_objs:
        i.draw()
    for i in time_objs:
        if i.time == 0:
            time_objs.pop(time_objs.index(i))

    base_pwr_up.draw()
    for i in pwr_up:
        i.draw()

    for i in enm:
        i.draw()

    if ply1.state == "move":
        ply1.draw()
    elif ply1.state == "die":
        ply1.death("end")
    elif ply1.state == "destroy":
        ply1.death("spawn")
    elif ply1.state == "spawn":
        ply1.spawn()

    for i in range(len(bull)):
        bull[i].draw()

    heart(life)
    pg.draw.rect(win, blue, (350, 7, int(80*ply1.eng/tot_eng), 12))
    win.blit(eng_bar, (350, 7))
    eng.draw()
    box_width = num_print(win, ply1.n_bull, 30, 5,
                          (245, 228, 24), (220, 136, 0))
    lvl_width = num_print(win, int(lvl), 258, 5)
    if ply1.n_bull > 0:
        try:
            win.blit(ply1.bull_icon[bull_anm_cnt//ply1.bull_anm], (5, 10))
        except IndexError:
            bull_anm_cnt = 0
        bull_anm_cnt += 1
        if bull_anm_cnt == len(ply1.bull_icon)*ply1.bull_anm:
            bull_anm_cnt = 0

    pg.display.update()


# buttons
resume = button(width/2-54, height/2-25, pause, 108, 32, 5)
quit_button = button(width/2-34, height/2+15, quit_button, 64, 32, 5)
next_button = button(430, 530, next_button, 64, 32, 5)
sfx_button = button(width/2-25, height/2+55, sfx, 44, 32, 5)
sfx2_button = button(width/2-25, height/2+55, sfx2, 44, 32, 5)
sound_button = button(width/2-50, height/2+95, sound, 96, 32, 5)
sound2_button = button(width/2-50, height/2+95, sound2, 96, 32, 5)
die_button = button(width/2-64, height/2-22, died,
                    died.get_width(), died.get_height(), 5)


run = True
cnt = 0

# menu
while run:
    clock.tick(fps)

    keys = pg.key.get_pressed()

    for event in pg.event.get():
        pos = pg.mouse.get_pos()

        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            click = True
        else:
            click = False

    if keys[pg.K_SPACE]:
        start_sound.play()
        run = False
        pg.time.delay(200)

    anm_img = crystal
    anm_fct = 1
    
    win.fill((0, 0, 0))
    win.blit(menu_txt[cnt//anm_fct//6], (100, 40))

    win.blit(anm_img[cnt//anm_fct//3], (width/2 -
                                     anm_img[0].get_width()/2, height/2-anm_img[0].get_height()/2))

    text_img = font3.render( 'Created By - Striker', 1, (117, 113, 97))
    win.blit(text_img, (320, 562))
    text_img = font3.render( 'Created By - Striker', 1, (223, 238, 215))
    win.blit(text_img, (320, 560))

    cnt += 1
    if cnt == len(anm_img)*anm_fct*3:
        cnt = 0

    pg.display.update()

run = True

# tutorial
dl_cnt = 0
while run:
    dl_cnt += 1 
    clock.tick(fps)

    keys = pg.key.get_pressed()

    for event in pg.event.get():
        pos = pg.mouse.get_pos()

        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            click = True
        else:
            click = False

        if click and next_button.isOver(pos) or keys[pg.K_SPACE] and dl_cnt>10:
            run = False

    text = ['1 You can kill enemy with dash','2 If you energy get low you will freeze','3 KiLL enemy to get your energy back','4 dash will gives more energy']
    win.fill((grnd))
    win.blit(tutorial[0], (-50, -20))
    for i in text:
        text_img = font1.render( i, 1, (117, 113, 97))
        win.blit(text_img, (30, 501+20*text.index(i)))
    for i in text:
        text_img = font1.render( i, 1, (223, 238, 215))
        win.blit(text_img, (30, 500+20*text.index(i)))
    text_img = font2.render( 'HOW TO PLAY', 1, (117, 113, 97))
    win.blit(text_img, (250, 44))
    text_img = font2.render( 'HOW TO PLAY', 1, (223, 238, 215))
    win.blit(text_img, (250, 40))
    next_button.draw(pos)

    pg.display.update()

game = True
while game:
    run = True
    pause = False
    click = True
    p_tim = 0
    ply1 = player(width/2, height/2, key_scrpt_2)
    enm_cnt = 0
    lvl = 1
    lvl_time = 0
    life = 3
    ply1.eng = tot_eng
    base_pwr_up = powerup(273, 100, blue_fire_prop)
    eng = powerup(348, -4, blue_fire_prop)
    pwr_up = []
    enm = []
    srt_enm = []
    time_objs = []
    pg.mixer.music.stop()
    bg_music = pg.mixer.music.load('sound/background2.mp3')
    pg.mixer.music.play(-1)

    # game
    while run:
        clock.tick(fps)
        lvl_time += 1

        keys = pg.key.get_pressed()

        # To quit the game
        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                click = True
            else:
                click = False

        if keys[pg.K_SPACE] and p_tim == 0:
            if pause:
                pg.mixer.music.unpause()
                p_tim = 1
                pause = False
            else:
                pg.mixer.music.pause()
                p_tim = 1
                pause = True

        if click and resume.isOver(pos):
            select_sound.play()
            pg.mixer.music.unpause()
            p_tim = 1
            pause = False
        if click and quit_button.isOver(pos):
            quit()

        if click and sfx_button.isOver(pos):
            pg.time.delay(200)
            if sfx_mute:
                sfx_mute = False
            else:
                sfx_mute = True

        if click and sound_button.isOver(pos):
            pg.time.delay(200)
            if music_mute:
                music_mute = False
            else:
                music_mute = True

        if pause:
            gameboard()
            resume.draw(pos)
            quit_button.draw(pos)

            if sfx_mute:
                sfx2_button.draw(pos)
            else:
                sfx_button.draw(pos)

            if music_mute:
                sound2_button.draw(pos)
            else:
                sound_button.draw(pos)

        if p_tim > 5:
            p_tim = 0

        if p_tim > 0:
            p_tim += 1

        if not pause:

            srt_enm = enm[:]
            srt_enm.sort(key=lambda x: distance(
                (ply1.x, ply1.y), (x.x, x.y)), reverse=True)

            if lvl % 7 == 0 and life < 4:
                lvl += .1
                life += 1
                slm_vel += 1

            if (lvl % 4 == 0 or (lvl > 10 and lvl % 2 and type(lvl) == int) or (lvl > 10 and lvl % 2 and type(lvl) == int) or (lvl_time % 400 == 0 and len(pwr_up) == 0) or not lvl_time % 1000) and lvl_time > 50:
                lvl += .1
                fct = 50
                tmp_x = random.randrange(
                    offset[0] + fct, width-fct - offset[2])
                tmp_y = random.randrange(fct + offset[1], height-fct-offset[3])

                lck = random.randrange(100)

                if lck >= 90:
                    tmp_prop = blast_prop
                elif lck >= 65:
                    tmp_prop = fire_wll_prop
                elif lck >= 40:
                    tmp_prop = spark_prop
                else:
                    tmp_prop = lrg_fire_prop

                tmp = powerup(tmp_x, tmp_y, tmp_prop)
                pwr_up.append(tmp)

            if keys[pg.K_e]:
                base_pwr_up.pickup(ply1)

            for i in pwr_up:
                if keys[pg.K_e] and i.pickup(ply1):
                    pwr_up.pop(pwr_up.index(i))
                if i.time_cnt > i.time:
                    pwr_up.pop(pwr_up.index(i))

            if len(pwr_up) > 3:
                pwr_up.pop(pwr_up.index(i))

            ply1.get_movements()
            ply1.move()
            ply1.cooldown()

            for i in srt_enm:
                chk = True
                for j in srt_enm:
                    if collide(i.img, j.img, i.x, i.y, j.x, j.y) and srt_enm.index(i) != srt_enm.index(j) and i.state == "move" and j.state == "move":
                        chk = False
                if chk == True:
                    i.move(ply1.x + char_width/2, ply1.y + char_height/2)
                else:
                    tmp = i.vel
                    i.vel = srt_enm.index(i) + 1
                    i.move(ply1.x + char_width/2, ply1.y + char_height/2)
                    i.vel = tmp

            for i in bull:
                if i.trvl_cnt >= i.trvl_dist:
                    bull.pop(bull.index(i))
                else:
                    i.move()

            if enm_cnt == 0:
                enm_cnt += 1
                enm.extend(gen_slm(int(enm_cnt), ply1.x, ply1.y))

            for i in enm:
                for j in bull:
                    if i.state == "move" and i.die(j.type[j.cnt//j.anm], j.x, j.y):
                        if ply1.eng < tot_eng:
                            ply1.eng += 5
                        if j.pen:
                            continue
                        bull.pop(bull.index(j))
                if ply1.dash:
                    if i.die(ply1.ply_img, ply1.x, ply1.y, False):
                        if ply1.eng < tot_eng:
                            ply1.eng += 10

            if len(enm) == 0:
                lvl = int(lvl)
                lvl += 1
                lvl_time = 0
                enm_cnt += 0.75
                enm.extend(gen_slm(int(enm_cnt), ply1.x, ply1.y))

            for i in enm:
                if i.state == "end":
                    rnd_img = random.choice(slm_spl)
                    ang = random.choice((0, 90, 280, 270))
                    rnd_img = pg.transform.rotate(rnd_img, ang)
                    tmp_spl = time_obj(i.x, i.y, rnd_img, 150)
                    time_objs.append(tmp_spl)
                    enm.pop(enm.index(i))

            for i in enm:
                if i.kill(ply1.ply_img, ply1.x, ply1.y) and not ply1.dash:
                    life -= 1
                    ply1.state = "destroy"
                    if life != 0:
                        death_sound.play()
                        dash_sound.play()
                    else:
                        hit_sound.play()
                        death_sound.play()
                        death2_sound.play()
                    for j in enm:
                        if distance((j.x, j.y), (ply1.x, ply1.y)) <= 100:
                            j.state = "die"
                if life == 0:
                    ply1.state = "die"

                if ply1.eng < tot_eng:
                    if ply1.f_tim[0] == 0:
                        ply1.eng += 0.05
                    else:
                        ply1.eng += 0.2
                else:
                    ply1.eng = tot_eng

            mute_sound(sfx_mute)
            mute_music(music_mute)
            redraw()
        pg.display.update()
        if ply1.state == "end":
            run = False

    run = True

    # exit
    while run:
        clock.tick(fps)
        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                click = True
            else:
                click = False

        if click and quit_button.isOver(pos):
            quit()
        if click and die_button.isOver(pos):
            select_sound.play()
            pg.time.delay(300)
            gameover_sound.stop()
            run = False

        gameboard()
        die_button.draw(pos)
        quit_button.draw(pos)
        pg.display.update()
