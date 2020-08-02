# coding=utf-8
import pygame
import os
import re
import threading

from settings import Settings


class Person():
    def __init__(self, screen, settings, file, name):
        self.screen = screen  # 设定位置
        self.settings = settings
        self.name = name

        self.image = pygame.image.load(file).convert_alpha()  # 加载图像
        self.rect = self.image.get_rect()  # 获取外接矩形
        self.screen_rect = screen.get_rect()  # 获取出来的外接矩形自带centerx,centery,top,bottom,left,right等属性

        self.rect.centerx = self.screen_rect.centerx
        # self.rect.bottom = self.screen_rect.bottom    # 每艘新飞船位于屏幕底部中央
        self.rect.centery = self.screen_rect.centery * 1.5

        self.show = False
        self.count = 0

    def update(self, file):
        self.image = pygame.image.load(file).convert_alpha()  # 加载图像
        self.rect = self.image.get_rect()  # 获取外接矩形
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery * 1.5

    def blitme(self):
        if self.show:
            blit_alpha(self.screen, self.image, (self.rect.x, self.rect.y), 256)
        else:
            blit_alpha(self.screen, self.image, (self.rect.x, self.rect.y), self.count)
            if self.count < 255:
                self.count += 5
            else:
                self.show = True
                self.count = 0


class Chat_rect():
    def __init__(self, Settings, screen, msg, name):
        self.screen = screen
        self.rect = pygame.Rect(
            0,  # 该矩形左边的坐标
            0,  # 该矩形上边的坐标
            Settings.chat_width,  # 宽度
            Settings.chat_height  # 高度/长度
        )
        self.rect.centerx = screen.get_rect().centerx
        self.rect.bottom = screen.get_rect().bottom * 0.95

        self.in_color = Settings.chat_maincolor
        self.side_color = Settings.chat_sidecolor
        self.text_color = Settings.chat_textcolor

        self.name_font = pygame.font.Font('fonts\\SourceHanSansCN-Normal.ttf', 30)
        self.text_font = pygame.font.Font('fonts\\SourceHanSansCN-Light.ttf', 28)
        self.name = name
        self.msg = msg

        self.count = 0
        self.show = True

        self.hide = True

    def update(self, name, msg):
        self.name = name
        self.msg = msg
        self.count = 0
        self.show = False
        self.hide = False

    def blit_name(self, name):
        self.name_image = self.name_font.render(
            name + ":",                    # 文本
            True,                   # 抗锯齿
            self.text_color,        # 文本颜色
            self.in_color       # 背景颜色
        )
        self.name_image_rect = self.name_image.get_rect()
        self.name_image_rect.top = self.rect.top + 5
        self.name_image_rect.left = self.rect.left + 20
        self.screen.blit(self.name_image, self.name_image_rect)

    def blit_msg(self, msg):
        x = self.name_image_rect.left
        y = self.name_image_rect.bottom
        token = 0
        for ch in msg:
            token += 1
            if token >= self.count:
                return
            word_surface = self.text_font.render(
                ch,
                True,
                self.text_color,
                self.in_color
            )
            word_width, word_height = word_surface.get_size()
            if x + word_width >= self.rect.right - 15:
                x = self.name_image_rect.left
                if y + word_height * 2 >= self.rect.bottom - 5:
                    raise Exception('Sentence_too_Long. Sentence is "{}"'.format(msg))
                y += word_height
            self.screen.blit(word_surface, (x, y))
            x += word_width
        self.show = True

    def show_msg(self, msg):
        self.blit_msg(msg)
        if self.count <= len(msg):
            self.count += 0.3

    def draw_chat(self):
        if not self.hide:
            pygame.draw.rect(self.screen, self.in_color, self.rect, 0)
            pygame.draw.rect(self.screen, self.side_color, self.rect, 5)
            self.blit_name(self.name)
            self.show_msg(self.msg)

    def is_showed(self):
        return self.show


dialog_ptr = 0
last_name = ''


def read_dialog(file='dialog.txt'):
    global dialog_ptr, last_name
    msg = ''
    event = 0
    name = ''
    """
    event == 0是正常对话
    -1是退出标志
    1是
    2是改变背景
    3是改变人物形象
    4是播放和停止BGM
    5是自动输入事件
    """
    with open(file, "r", encoding='utf-8') as fp:
        fp.seek(dialog_ptr)
        try:
            line = fp.readline()
            while True:
                if line[-2] == ':' or line[-2] == '：':
                    last_name = line[:-2]
                    name = last_name
                    line = fp.readline()
                elif re.search(r'''^  (.+?)$''', line):
                    event = 0
                    name = last_name
                    msg = re.search(r'''^  (.+?)$''', line).group(1).strip()
                    break
                elif re.search(r'''^\[bg\s*?=\s*?'(.+?)'\]$''', line):
                    event = 2
                    msg = re.search(r'''^\[bg\s*?=\s*?'(.+?)'\]$''', line).group(1)
                    break
                elif re.search(r'''^\[name\s*?=\s*?'(.+?)'(.+?)img\s*?=\s*?'(.+?)'\]$''', line):
                    event = 3
                    msg = re.search(r'''^\[name\s*?=\s*?'(.+?)'(.+?)img\s*?=\s*?'(.+?)'\]$''', line).group(3)
                    name = re.search(r'''^\[name\s*?=\s*?'(.+?)'(.+?)img\s*?=\s*?'(.+?)'\]$''', line).group(1)
                    break
                elif re.search(r'''^\[music\s*?=\s*?'(.+?)'\]$''', line):
                    event = 4
                    msg = re.search(r'''^\[music\s*?=\s*?'(.+?)'\]$''', line).group(1)
                    break
                elif re.search(r'''^\[event\s*?=\s*?'(.+?)'\]$''', line):
                    event = 5
                    msg = re.search(r'''^\[event\s*?=\s*?'(.+?)'\]$''', line).group(1)
                    break
                else:
                    line = fp.readline()
        except IndexError:
            print(msg, name)
            event = -1
        dialog_ptr = fp.tell()

    return name, msg, event


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def switch_bg_proc(screen, after, before):
    global ticks
    ticks = 0
    while ticks < 255:
        blit_alpha(screen, before, (0, 0), 260 - ticks)
        blit_alpha(screen, after, (0, 0), ticks)
        yield
    blit_alpha(screen, after, (0, 0), 256)
    ticks = 0


def chg_bg(screen, msg, before, sbp):
    global ticks, sbp_flag
    after = pygame.image.load('imgs/{}'.format(msg)).convert()
    if sbp_flag:
        print("!!!!")
        ticks = 254
    else:
        sbp = switch_bg_proc(screen, after, before)
        sbp_flag = True

    return after, sbp


def chg_ch(people, msg, name, screen, game_set):
    if msg == 'del':
        del people[name]
    elif name not in people:
        people[name] = Person(screen, game_set, 'imgs/{}'.format(msg), name)
    else:
        people[name].update('imgs/{}'.format(msg))


def play_music(music_file):
    global bgm_flag
    '''
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    '''
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 2048  # number of samples (experiment to get right sound)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(1.0)
    clock = pygame.time.Clock()
    music_file = "bgm/{}".format(music_file)
    try:
        pygame.mixer.music.load(music_file)
        # print("Music file {} loaded!".format(music_file))
    except pygame.error:
        print("File {} not found! {}".format(music_file, pygame.get_error()))
        return
    pygame.mixer.music.play(-1, 0)      # 第一个参数是-1的话会循环播放，是0则播放一次
    # check if playback has finished
    while pygame.mixer.music.get_busy() and bgm_flag:
        clock.tick(60)

    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()


def chg_bgm(msg: str):
    global play_bgm, bgm_flag
    if msg == 'stop':
        bgm_flag = False
        return
    if play_bgm.is_alive():
        pass
    else:
        bgm_flag = True
        play_bgm = threading.Thread(target=play_music, args=(msg, ))
        play_bgm.setDaemon(True)
        play_bgm.start()


def auto_event(msg: str):
    desti = 'pygame.{}'.format(msg)
    pygame.event.post(pygame.event.Event(eval(desti)))


ticks = 0
sbp_flag = False
play_bgm = threading.Thread()
bgm_flag = False


def main():
    global ticks, sbp_flag
    pygame.init()
    pygame.display.set_caption("small game")
    game_set = Settings()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((game_set.screen_width, game_set.screen_height))
    # bg = (0, 0, 0)
    people = {}
    background = pygame.image.load("imgs/bg_black.jpg").convert()
    blit_alpha(screen, background, (0, 0), 256)
    name, msg = '', ''
    chat = Chat_rect(
        game_set,
        screen,
        msg,
        name
    )
    sbp = None

    os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(game_set.window_pos_x, game_set.window_pos_y)

    while True:
        for in_event in pygame.event.get():
            if in_event.type == pygame.QUIT:
                pygame.display.quit()
                return
            elif in_event.type == pygame.MOUSEBUTTONDOWN: #  and pygame.mouse.get_pressed()[0]:
                if sbp_flag:
                    ticks = 254
                    continue

                conti_flag = False
                for person in people:
                    if not people[person].show:
                        people[person].show = True
                        conti_flag = True
                if conti_flag:
                    continue

                if not chat.is_showed():
                    chat.show = True
                    chat.count = 100
                    continue

                name, msg, game_event = read_dialog()
                if game_event == 0:
                    chat.update(name, msg)
                elif game_event == -1:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif game_event == 1:
                    pass
                elif game_event == 2:
                    background, sbp = chg_bg(screen, msg, background, sbp)
                elif game_event == 3:
                    chg_ch(people, msg, name, screen, game_set)
                elif game_event == 4:
                    chg_bgm(msg)
                elif game_event == 5:
                    auto_event(msg)
            '''elif in_event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                if sbp_flag:
                    ticks = 254'''

        if sbp_flag:
            ticks += 5
            try:
                next(sbp)
            except StopIteration:
                sbp_flag = False
        else:
            blit_alpha(screen, background, (0, 0), 256)

        for i in people:
            people[i].blitme()
        chat.draw_chat()
        pygame.display.flip()

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()
