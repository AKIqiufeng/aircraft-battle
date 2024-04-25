import pygame as pg

pg.init()
screen = pg.display.set_mode((480, 700))
pg.display.set_caption("Aircraft Battle")
bg = pg.image.load("./resource/image/background.png")
bgRect = bg.get_rect()
bgRect.center = (240, 350)
me = pg.image.load("./resource/image/me2.png")
meRect = me.get_rect()
meRect.center = (240, 350)

while True:
    screen.fill("white")
    screen.blit(bg, bgRect)
    screen.blit(me, meRect)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                meRect.x -= 30
            elif event.key == pg.K_RIGHT:
                meRect.x += 30
            elif event.key == pg.K_UP:
                meRect.y -= 30
            elif event.key == pg.K_DOWN:
                meRect.y += 30
    pg.display.flip()
