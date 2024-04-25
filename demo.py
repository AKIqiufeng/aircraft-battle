import pygame as pg
from pygame.locals import *
import os

WIDTH = 480
HEIGHT = 700


def load_animation(imageName):
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


class Player:
    def __init__(self):
        self.images = load_animation("./resource/image/me{}.png")
        self.imageIdx = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT))
        self.move = [0, 0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        self.rect.x += self.move[0]
        self.rect.y += self.move[1]

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def update_idx(self):
        self.imageIdx += 1
        self.image = self.images[self.imageIdx % len(self.images)]


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    bg = pg.image.load("./resource/image/background.png")
    bgRect = bg.get_rect()
    bgRect.topleft = (0, 0)

    player = Player()
    speed = 5

    moving = pg.event.Event(USEREVENT)
    pg.time.set_timer(moving, 100)

    while True:
        pg.display.set_caption(str(clock.get_fps()))
        screen.fill("white")
        screen.blit(bg, bgRect)

        player.draw(screen)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.move[0] -= speed
                elif event.key == K_RIGHT:
                    player.move[0] += speed
                elif event.key == K_UP:
                    player.move[1] -= speed
                elif event.key == K_DOWN:
                    player.move[1] += speed

            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    player.move[0] = 0
                elif event.key == K_RIGHT:
                    player.move[0] = 0
                elif event.key == K_UP:
                    player.move[1] = 0
                elif event.key == K_DOWN:
                    player.move[1] = 0

            elif event.type == moving.type:
                player.update_idx()

        clock.tick(144)
        pg.display.flip()


if __name__ == "__main__":
    main()
