import pygame as pg
import os

pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()

# constants
# dimension of window
width = 512
height = 560

# offset
offset = [10, 80, 13, 55]

# dimension of player
char_width = 64
char_height = 64
# dimension of border
b_width = 13


# slime  enemey
slm_size = 20
slm_vel = 3


# hair colours
skn = (245, 183, 132)
dskn = (218, 101, 94)
gry = (120, 120, 120)
dgry = (40, 40, 40)
red = (224, 60, 40)
dred = (130, 60, 61)
blue = (32, 176, 216)
dblue = (32, 100, 216)
green = (108, 216, 32)
grnd = (72, 59, 58)

# speed constants
max_vel = 8
sprnt = 16
acc = 4
d_acc = 4
int_vel = 2
dash = 2
bul_vel = 25
wall_bon = 20
w_stun = 5
# frame per second
fps = 16
idle = [0, 0, 0, 0, 1, 2, 2, 1]
i_cnt = 0
n_bull = 0
tot_eng = 120
# movments keys dash-sprint-fire-up-down-left-right
key_scrpt_1 = [pg.K_SPACE, pg.K_LSHIFT, pg.K_f, pg.K_w, pg.K_s, pg.K_a, pg.K_d]
key_scrpt_2 = [pg.K_x, pg.K_z, pg.K_c,
               pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT]

font1 = pg.font.SysFont('font', 20)
font2 = pg.font.SysFont('font', 50)
font3 = pg.font.SysFont('font', 30)


bg = [pg.transform.scale(pg.image.load('images/background_1.png'), (width, height)), pg.transform.scale(pg.image.load('images/background_2.png'), (width, height)),
      pg.transform.scale(pg.image.load('images/background_3.png'), (width, height))]

icon = pg.image.load("images/icon.png")

digit = [pg.image.load('images/digit/0.png'), pg.image.load('images/digit/1.png'), pg.image.load('images/digit/2.png'), pg.image.load('images/digit/3.png'), pg.image.load('images/digit/4.png'),
         pg.image.load('images/digit/5.png'), pg.image.load('images/digit/6.png'), pg.image.load('images/digit/7.png'), pg.image.load('images/digit/8.png'), pg.image.load('images/digit/9.png')]

died = pg.transform.scale(pg.image.load('images/hud/died.png'), (128, 32))
sfx = pg.transform.scale(pg.image.load('images/hud/sfx.png'), (44, 32))
sfx2 = pg.transform.scale(pg.image.load('images/hud/sfx2.png'), (44, 32))
sound = pg.transform.scale(pg.image.load('images/hud/sound.png'), (96, 32))
sound2 = pg.transform.scale(pg.image.load('images/hud/sound2.png'), (96, 32))

health = [pg.image.load('images/hud/heart_1.png'),
          pg.image.load('images/hud/heart_2.png')]
eng_bar = pg.transform.scale(pg.image.load('images/hud/eng_bar.png'), (80, 12))

coin = [pg.image.load('images/coin/coin_1.png'), pg.image.load('images/coin/coin_2.png'),
        pg.image.load('images/coin/coin_3.png'), pg.image.load('images/coin/coin_4.png')]
coin = [pg.transform.scale(x, (50, 50)) for x in coin]
coin_s = [pg.transform.scale(x, (20, 20)) for x in coin]

crystal = [pg.image.load('images/crystal/crystal_1.png'), pg.image.load('images/crystal/crystal_2.png'),
           pg.image.load('images/crystal/crystal_3.png'), pg.image.load('images/crystal/crystal_4.png')]
crystal = [pg.transform.scale(x, (20, 48)) for x in crystal]
crystal_s = [pg.transform.scale(x, (10, 24)) for x in crystal]

b_crystal = [pg.image.load('images/b_crystal/b_crystal_1.png'), pg.image.load('images/b_crystal/b_crystal_2.png'),
             pg.image.load('images/b_crystal/b_crystal_3.png'), pg.image.load('images/b_crystal/b_crystal_4.png')]
b_crystal_s = [pg.transform.scale(x, (10, 24)) for x in b_crystal]
b_crystal_prop = (b_crystal_s, 2, [], [], False, 1, 0, 0)

slm_spl = [pg.image.load('images/splash/spl_1.png'), pg.image.load(
    'images/splash/spl_2.png'), pg.image.load('images/splash/spl_3.png')]
slm_spl = [pg.transform.scale(x, (32, 32)) for x in slm_spl]

move_down = [pg.image.load(os.path.join('images/down', 'move_down (1).png')), pg.image.load(os.path.join('images/down', 'move_down (2).png')),
             pg.image.load(os.path.join('images/down', 'move_down (3).png')), pg.image.load(os.path.join('images/down', 'move_down (4).png'))]
move_up = [pg.image.load(os.path.join('images/up', 'move_up (1).png')), pg.image.load(os.path.join('images/up', 'move_up (2).png')),
           pg.image.load(os.path.join('images/up', 'move_up (3).png')), pg.image.load(os.path.join('images/up', 'move_up (4).png'))]
move_left = [pg.image.load(os.path.join('images/left', 'move_left (1).png')), pg.image.load(os.path.join('images/left', 'move_left (2).png')),
             pg.image.load(os.path.join('images/left', 'move_left (3).png')), pg.image.load(os.path.join('images/left', 'move_left (4).png'))]
move_right = [pg.image.load(os.path.join('images/right', 'move_right (1).png')), pg.image.load(os.path.join('images/right', 'move_right (2).png')),
              pg.image.load(os.path.join('images/right', 'move_right (3).png')), pg.image.load(os.path.join('images/right', 'move_right (4).png'))]


dsh = [pg.image.load(os.path.join('images/dash', 'dash_u.png')), pg.image.load(os.path.join('images/dash', 'dash_r.png')),
       pg.image.load(os.path.join('images/dash', 'dash_d.png')), pg.image.load(os.path.join('images/dash', 'dash_l.png')), ]

walk_eff = [pg.image.load(os.path.join('images/walk', 'walk_eff (1).png')), pg.image.load(os.path.join('images/walk', 'walk_eff (2).png')),
            pg.image.load(os.path.join('images/walk', 'walk_eff (3).png')), pg.image.load(os.path.join('images/walk', 'walk_eff (4).png'))]


wall_eff = [(pg.image.load(os.path.join('images', 'wll_2.png'))),
            (pg.image.load(os.path.join('images', 'wll_1.png')))]

lrg_fire = [pg.transform.scale(pg.image.load('images/bullets/fire (1).png'), (24, 40)), pg.transform.scale(pg.image.load('images/bullets/fire (2).png'), (24, 40)), pg.transform.scale(pg.image.load('images/bullets/fire (3).png'), (24, 40)), pg.transform.scale(pg.image.load('images/bullets/fire (4).png'), (24, 40)),
            pg.transform.scale(pg.image.load('images/bullets/fire (5).png'), (24, 40)), pg.transform.scale(pg.image.load('images/bullets/fire (6).png'), (24, 40)), pg.transform.scale(pg.image.load('images/bullets/fire (7).png'), (24, 40)), pg.transform.scale(pg.image.load('images/bullets/fire (8).png'), (24, 40))]
lrg_firep = [pg.transform.scale(x, (16, 25)) for x in lrg_fire]
lrg_fire_trvl = 30
lrg_fire_prop = (lrg_firep, 1, lrg_fire, lrg_fire_trvl, True, 1, 10, 30)

blue_fire = [pg.image.load('images/blue_fire/blue_fire_1.png'), pg.image.load('images/blue_fire/blue_fire_2.png'), pg.image.load('images/blue_fire/blue_fire_3.png'), pg.image.load('images/blue_fire/blue_fire_4.png'), pg.image.load('images/blue_fire/blue_fire_5.png'), pg.image.load('images/blue_fire/blue_fire_6.png'), pg.image.load('images/blue_fire/blue_fire_7.png'), pg.image.load('images/blue_fire/blue_fire_8.png'), pg.image.load('images/blue_fire/blue_fire_9.png'), pg.image.load('images/blue_fire/blue_fire_10.png'), pg.image.load('images/blue_fire/blue_fire_11.png'), pg.image.load('images/blue_fire/blue_fire_12.png'), pg.image.load('images/blue_fire/blue_fire_13.png'), pg.image.load('images/blue_fire/blue_fire_14.png'), pg.image.load('images/blue_fire/blue_fire_15.png'), pg.image.load('images/blue_fire/blue_fire_16.png'), pg.image.load('images/blue_fire/blue_fire_17.png'), pg.image.load('images/blue_fire/blue_fire_18.png'), pg.image.load('images/blue_fire/blue_fire_19.png'), pg.image.load('images/blue_fire/blue_fire_20.png'), pg.image.load('images/blue_fire/blue_fire_21.png'), pg.image.load('images/blue_fire/blue_fire_22.png'), pg.image.load('images/blue_fire/blue_fire_23.png'), pg.image.load('images/blue_fire/blue_fire_24.png'), pg.image.load('images/blue_fire/blue_fire_25.png'), pg.image.load('images/blue_fire/blue_fire_26.png'), pg.image.load('images/blue_fire/blue_fire_27.png'), pg.image.load('images/blue_fire/blue_fire_28.png'), pg.image.load('images/blue_fire/blue_fire_29.png'), pg.image.load('images/blue_fire/blue_fire_30.png'),
             pg.image.load('images/blue_fire/blue_fire_31.png'), pg.image.load('images/blue_fire/blue_fire_32.png'), pg.image.load('images/blue_fire/blue_fire_33.png'), pg.image.load('images/blue_fire/blue_fire_34.png'), pg.image.load('images/blue_fire/blue_fire_35.png'), pg.image.load('images/blue_fire/blue_fire_36.png'), pg.image.load('images/blue_fire/blue_fire_37.png'), pg.image.load('images/blue_fire/blue_fire_38.png'), pg.image.load('images/blue_fire/blue_fire_39.png'), pg.image.load('images/blue_fire/blue_fire_40.png'), pg.image.load('images/blue_fire/blue_fire_41.png'), pg.image.load('images/blue_fire/blue_fire_42.png'), pg.image.load('images/blue_fire/blue_fire_43.png'), pg.image.load('images/blue_fire/blue_fire_44.png'), pg.image.load('images/blue_fire/blue_fire_45.png'), pg.image.load('images/blue_fire/blue_fire_46.png'), pg.image.load('images/blue_fire/blue_fire_47.png'), pg.image.load('images/blue_fire/blue_fire_48.png'), pg.image.load('images/blue_fire/blue_fire_49.png'), pg.image.load('images/blue_fire/blue_fire_50.png'), pg.image.load('images/blue_fire/blue_fire_51.png'), pg.image.load('images/blue_fire/blue_fire_52.png'), pg.image.load('images/blue_fire/blue_fire_53.png'), pg.image.load('images/blue_fire/blue_fire_54.png'), pg.image.load('images/blue_fire/blue_fire_55.png'), pg.image.load('images/blue_fire/blue_fire_56.png'), pg.image.load('images/blue_fire/blue_fire_57.png'), pg.image.load('images/blue_fire/blue_fire_58.png'), pg.image.load('images/blue_fire/blue_fire_59.png'), pg.image.load('images/blue_fire/blue_fire_60.png')]
blue_fire = [pg.transform.scale(x, (10, 25)) for x in blue_fire]
blue_fire_trvl = 30
blue_fire_prop = (blue_fire, 1, blue_fire, blue_fire_trvl, False, 1, 20, 20)

blast = [pg.image.load('images/blast/blast_1.png'), pg.image.load(
    'images/blast/blast_2.png')]
blast = [pg.transform.scale(x, (70, 70)) for x in blast]
blast_trvl = 30
blast_prop = (crystal_s, 2, blast, blast_trvl, True, 1, 2, 120)

spark = [pg.image.load('images/spark/spark_1.png'), pg.image.load('images/spark/spark_2.png'), pg.image.load('images/spark/spark_3.png'), pg.image.load('images/spark/spark_4.png'),
         pg.image.load('images/spark/spark_5.png'), pg.image.load('images/spark/spark_6.png'), pg.image.load('images/spark/spark_7.png'), pg.image.load('images/spark/spark_8.png')]
spark = [pg.transform.scale(x, (40, 40)) for x in spark]
spark_p = [pg.transform.scale(x, (20, 20)) for x in spark]
spark_trvl = 30
spark_prop = (spark_p, 2, spark, spark_trvl, True, 1, 5, 60)

fire_wll = [pg.image.load('images/fire_wll/fire_wll_1.png'), pg.image.load('images/fire_wll/fire_wll_2.png'), pg.image.load('images/fire_wll/fire_wll_3.png'),
            pg.image.load('images/fire_wll/fire_wll_4.png'), pg.image.load('images/fire_wll/fire_wll_5.png'), pg.image.load('images/fire_wll/fire_wll_6.png')]
fire_wll = [pg.transform.scale(x, (30, 50)) for x in fire_wll]
fire_wll_trvl = 6
fire_wll_prop = (coin_s, 2, fire_wll, fire_wll_trvl, True, 1, 5, 50)

slm_s = [pg.image.load('images/slm_s/slm_s_1.png'), pg.image.load('images/slm_s/slm_s_2.png'),
         pg.image.load('images/slm_s/slm_s_3.png'), pg.image.load('images/slm_s/slm_s_4.png')]
slm_f = [pg.image.load('images/slm_f/slm_f_1.png'), pg.image.load('images/slm_f/slm_f_2.png'),
         pg.image.load('images/slm_f/slm_f_3.png'), pg.image.load('images/slm_f/slm_f_4.png')]
slm_b = [pg.image.load('images/slm_b/slm_b_1.png'), pg.image.load('images/slm_b/slm_b_2.png'),
         pg.image.load('images/slm_b/slm_b_3.png'), pg.image.load('images/slm_b/slm_b_4.png')]
slm_spawn = [pg.image.load('images/slm_spawn/slm_spawn_1.png'), pg.image.load('images/slm_spawn/slm_spawn_2.png'), pg.image.load('images/slm_spawn/slm_spawn_3.png'),
             pg.image.load('images/slm_spawn/slm_spawn_4.png'), pg.image.load('images/slm_spawn/slm_spawn_5.png')]
slm_die = [pg.image.load('images/slm_die/slm_die_1.png'), pg.image.load('images/slm_die/slm_die_2.png'), pg.image.load('images/slm_die/slm_die_3.png'), pg.image.load('images/slm_die/slm_die_4.png'),
           pg.image.load('images/slm_die/slm_die_5.png'), pg.image.load('images/slm_die/slm_die_6.png'), pg.image.load('images/slm_die/slm_die_7.png'), pg.image.load('images/slm_die/slm_die_8.png')]
slm_dieb = [pg.image.load('images/slm_dieb/slm_die_1.png'), pg.image.load('images/slm_dieb/slm_die_2.png'), pg.image.load('images/slm_dieb/slm_die_3.png'), pg.image.load('images/slm_dieb/slm_die_4.png'),
            pg.image.load('images/slm_dieb/slm_die_5.png'), pg.image.load('images/slm_dieb/slm_die_6.png'), pg.image.load('images/slm_dieb/slm_die_7.png'), pg.image.load('images/slm_dieb/slm_die_8.png')]

pause = pg.transform.scale(pg.image.load('images/hud/pause.png'), (108, 32))
quit_button = pg.transform.scale(
    pg.image.load('images/hud/quit.png'), (64, 32))
next_button = pg.transform.scale(
    pg.image.load('images/hud/next.png'), (64, 32))
menu_txt = [pg.transform.scale(pg.image.load('images/hud/menu_txt.png'), (300, 450)),pg.transform.scale(pg.image.load('images/hud/menu_txt2.png'), (300, 450))]
tutorial = [pg.transform.scale(pg.image.load('images/hud/tutorial_1.png'), (312*2, 317*2)),
            pg.transform.scale(pg.image.load('images/hud/tutorial_2.png'), (312*2, 317*2))]

shock = [pg.image.load('images/shock/shock_1.png'), pg.image.load('images/shock/shock_2.png'), pg.image.load('images/shock/shock_3.png'), pg.image.load('images/shock/shock_4.png'), pg.image.load(
    'images/shock/shock_5.png'), pg.image.load('images/shock/shock_6.png'), pg.image.load('images/shock/shock_7.png'), pg.image.load('images/shock/shock_8.png'), pg.image.load('images/shock/shock_9.png'), pg.image.load('images/shock/shock_10.png')]
shock = [pg.transform.scale(x, (150, 150)) for x in shock]

# musics
sfx_mute = False
music_mute = False
pg.mixer.music.load('sound/menu.mp3')

hit_sound = pg.mixer.Sound('sound/hit.wav')
fire_sound = pg.mixer.Sound('sound/fire.wav')
spark_sound = pg.mixer.Sound('sound/spark.wav')
spark2_sound = pg.mixer.Sound('sound/spark2.wav')
blast_sound = pg.mixer.Sound('sound/blast.wav')
blast2_sound = pg.mixer.Sound('sound/blast2.wav')
dash_sound = pg.mixer.Sound('sound/dash.wav')
wall_hit_sound = pg.mixer.Sound('sound/wall_hit.wav')
sprint_sound = pg.mixer.Sound('sound/sprint.wav')
death_sound = pg.mixer.Sound('sound/death.wav')
death2_sound = pg.mixer.Sound('sound/death2.wav')
gameover_sound = pg.mixer.Sound('sound/gameover.wav')
select_sound = pg.mixer.Sound('sound/select.wav')
start_sound = pg.mixer.Sound('sound/start.wav')


win = pg.display.set_mode((width+10, height+30))
pg.display.set_caption("Blast - Showdown Battle")
pg.display.set_icon(icon)
pg.mixer.music.play(-1)
clock = pg.time.Clock()
