from random import randint
import pygame as pg
from pygame.locals import *
import os


WIDTH = 480
HEIGHT = 700
PLAYERSPEED = 5
BULLETSPEED = 5
ENEMYSPEED = 1
ENEMYRATES = 1000
BULLETRATES = 200


def load_animation(imageName):  # 加载帧序列图片
    images = []
    count = 0
    while True:
        count += 1
        fileName = imageName.format(count)
        if os.path.exists(fileName):
            images.append(pg.image.load(fileName))
        else:
            break
    return images


def collide_mask(mask1, mask2, pos1, pos2):  # 用于检测Mask碰撞的函数
    return mask1.overlap(mask2, (pos2[0] - pos1[0], pos2[1] - pos1[1]))


class Player(pg.sprite.Sprite):  # 玩家类
    def __init__(self, *group):
        super().__init__(*group)

        self.images = load_animation("./resource/image/me{}.png")
        self.imageIdx = 0
        self.lastAniTime = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT))
        self.mask = pg.mask.from_surface(self.image)
        self.downImages = load_animation("./resource/image/me_destroy_{}.png")
        self.downIdx = 0

        self.lifeNum = 3

    def update(self):  # 更新玩家图片，实现动画效果
        for enemy1 in enemy_group:  # 遍历敌机组（也可以写成enemy_group.sprites()）
            if collide_mask(self.mask, enemy1.mask, self.rect, enemy1.rect):  # 判断玩家是否与敌机发生碰撞
                enemy1.kill()
                self.lifeNum -= 1
                if self.lifeNum == 0:
                    pg.quit()

        nowtime = pg.time.get_ticks()
        if nowtime - self.lastAniTime > 100:
            self.lastAniTime = nowtime
            self.imageIdx += 1
            self.image = self.images[self.imageIdx % len(self.images)]

        key = pg.key.get_pressed()  # 读取键盘移动，按下时持续移动
        if key[K_LEFT]:
            self.rect.x -= PLAYERSPEED
        elif key[K_RIGHT]:
            self.rect.x += PLAYERSPEED
        if key[K_UP]:
            self.rect.y -= PLAYERSPEED
        elif key[K_DOWN]:
            self.rect.y += PLAYERSPEED

        if self.rect.left < 0:  # 移动到边界判断
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Enemy1(pg.sprite.Sprite):  # 敌人1类
    def __init__(self, *group):
        super().__init__(*group)

        self.image = pg.image.load("./resource/image/enemy1.png")
        self.rect = self.image.get_rect(bottom=0, centerx=randint(29, WIDTH-29))
        self.mask = pg.mask.from_surface(self.image)
        self.lastAniTime = 0
        self.downImages = load_animation("./resource/image/enemy1_down{}.png")
        self.downIdx = 0
        self.die = 0
        self.sound = pg.mixer.Sound("./resource/sound/enemy1_down.wav")

    def update(self):

        self.rect.y += ENEMYSPEED  # 移动敌机
        if self.rect.y > HEIGHT:  # 如果敌机飞出屏幕则移除此精灵
            self.kill()

        nowtime = pg.time.get_ticks()
        if nowtime - self.lastAniTime > 100:
            self.lastAniTime = nowtime
            if self.die == 1:
                if self.downIdx == 0:
                    self.sound.play()
                self.downIdx += 1
                self.image = self.downImages[self.downIdx % len(self.downImages)]
                if self.downIdx > 3:
                    self.kill()


class Bullet(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pg.image.load("./resource/image/bullet1.png")
        self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= BULLETSPEED
        if self.rect.bottom < 0:  # 如果子弹飞出屏幕则移除此精灵
            self.kill()


pg.init()  # 初始化
pg.mixer.pre_init()

screen = pg.display.set_mode((WIDTH, HEIGHT))  # 设置窗口大小
clock = pg.time.Clock()  # 设置时钟，用以帧数控制
pg.display.set_caption("飞机大战")  # 窗口标题


pg.mixer.music.load("./resource/sound/game_music.ogg")  # 设置背景音乐
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.5)

bg = pg.image.load("./resource/image/background.png")  # 加载背景图片
bgRect = bg.get_rect()
bgRect.topleft = (0, 0)

all_group = pg.sprite.Group()
enemy_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()

player = Player(all_group)  # 实例化玩家飞机对象
# 设置初始移动速度

last_add_enemy = 0
last_add_bullet = 0
enemy1Num = 2

while True:

    screen.blit(bg, bgRect)  # 显示背景图片
    all_group.draw(screen)  # 绘制所有对象

    all_group.update()

    col = pg.sprite.groupcollide(bullet_group, enemy_group, True, False)
    for enemys in col.values():
        for enemy in enemys:
            enemy.die = 1

    now = pg.time.get_ticks()  # 获取游戏运行时间(ms)
    if now - last_add_enemy > ENEMYRATES:  # 每隔ENEMYRATES毫秒添加一次敌机
        last_add_enemy = now
        for i in range(enemy1Num):
            enemy_group.add(Enemy1(all_group, enemy_group))

    if now - last_add_bullet > BULLETRATES:
        last_add_bullet = now
        bullet_group.add(Bullet(all_group, bullet_group))

    for event in pg.event.get():  # 读取事件列表
        if event.type == QUIT:  # 退出事件
            pg.quit()

    clock.tick(144)  # 最大帧率设置为144
    pg.display.flip()  # 刷新绘制内容
