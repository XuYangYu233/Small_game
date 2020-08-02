# coding=utf-8
import pygame
import sys

pygame.init()
size = width, height = 1345, 650
bg = (0, 0, 0)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("alpha通道尝试2，淡化转场尝试")

black = pygame.image.load("imgs/bg_拟生树海.jpg").convert()
hallway = pygame.image.load("imgs/bg_中国风走廊.jpg").convert()

position = black.get_rect()
position.center = width // 2, height // 2


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def switch_bg_proc(screen, hallway, black):
    global ticks
    ticks = 0
    while ticks < 255:
        blit_alpha(screen, black, (0, 0), 260 - ticks)
        blit_alpha(screen, hallway, (0, 0), ticks)
        yield
    blit_alpha(screen, hallway, (0, 0), 255)
    ticks = 0


ticks = 0
sbp_flag = False
blit_alpha(screen, black, (0, 0), 260-ticks)
# 设置为死循环，确保窗口一直显示
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if not sbp_flag:
                sbp = switch_bg_proc(screen, hallway, black)
                sbp_flag = True
            else:
                ticks = 254

    if sbp_flag:
        ticks += 5
        try:
            next(sbp)
        except StopIteration:
            sbp_flag = False
    pygame.display.flip()

    clock.tick(60)
    pygame.display.update()
