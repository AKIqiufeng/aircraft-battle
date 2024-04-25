import pygame as pg
from pygame.locals import *
import os

WIDTH = 480
HEIGHT = 700


def load_animation(imageName):  # 加载帧序列图片
    images = []
    i = 0
    while True:
        i += 1
        fileName = imageName.format(i)
        if os.path.exists(fileName):
            images.append(pg.image.load(fileName))
        else:
            break
    return images


class Player:  # 玩家类
    def __init__(self):
        self.images = load_animation("./resource/image/me{}.png")
        self.imageIdx = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT))
        self.move = [0, 0]

    def draw(self, screen):  # 绘制玩家飞机
        screen.blit(self.image, self.rect)

        self.rect.x += self.move[0]  # 更新移动后坐标
        self.rect.y += self.move[1]

        if self.rect.left < 0:  # 移动到边界判断
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def update_idx(self):  # 更新玩家图片，实现动画效果
        self.imageIdx += 1
        self.image = self.images[self.imageIdx % len(self.images)]


def main():
    pg.init()  # 初始化
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 设置窗口大小
    clock = pg.time.Clock()  # 设置时钟，用以帧数控制
    pg.display.set_caption("飞机大战")  # 窗口标题

    bg = pg.image.load("./resource/image/background.png")  # 加载背景图片
    bgRect = bg.get_rect()
    bgRect.topleft = (0, 0)

    player = Player()  # 实例化玩家飞机对象
    speed = 5  # 设置初始移动速度

    moving = pg.event.Event(USEREVENT)  # 定义移动事件 用以更新动画
    pg.time.set_timer(moving, 100)  # 移动事件每0.1秒触发一次

    while True:

        screen.blit(bg, bgRect)  # 显示背景图片
        player.draw(screen)  # 绘制玩家飞机

        for event in pg.event.get():  # 读取事件列表
            if event.type == QUIT:  # 退出事件
                pg.quit()

            elif event.type == KEYDOWN:  # 读取键盘移动，按下时持续移动
                if event.key == K_LEFT:
                    player.move[0] -= speed
                elif event.key == K_RIGHT:
                    player.move[0] += speed
                elif event.key == K_UP:
                    player.move[1] -= speed
                elif event.key == K_DOWN:
                    player.move[1] += speed

            elif event.type == KEYUP:  # 松手时不移动
                if event.key == K_LEFT:
                    player.move[0] = 0
                elif event.key == K_RIGHT:
                    player.move[0] = 0
                elif event.key == K_UP:
                    player.move[1] = 0
                elif event.key == K_DOWN:
                    player.move[1] = 0

            elif event.type == moving.type:  # 读取移动事件，更新玩家飞机图片
                player.update_idx()

        clock.tick(144)  # 最大帧率设置为144
        pg.display.flip()  # 刷新绘制内容


if __name__ == "__main__":
    main()
