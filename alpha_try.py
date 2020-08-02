# coding=utf-8
import pygame
import sys
import threading

# from pygame.locals import *

pygame.init()
size = width, height = 1345, 650
bg = (0, 0, 0)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("初次见面，请大家多多关照")

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
        pygame.display.flip()
    blit_alpha(screen, hallway, (0, 0), 255)
    pygame.display.flip()
    ticks = 0


ticks = 0
t_s = threading.Thread()
blit_alpha(screen, black, (0, 0), 260-ticks)
# 设置为死循环，确保窗口一直显示
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if t_s.is_alive():
                ticks = 254
            else:
                t_s = threading.Thread(target=switch_bg_proc, args=(screen, hallway, black))
                t_s.start()
            # switch_proc(screen, hallway, black)

    # 更新图像
    # screen.blit(hallway, (0, 0))

    # 更新界面

    if t_s.is_alive():
        ticks += 5
    else:
        pygame.display.flip()

    clock.tick(60)
    pygame.display.update()
