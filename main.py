import pygame
import os
import sys
import time
import random


FPS = 50

pygame.init()
size = width, height = 400, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
SPEED = 4
enemy_group = pygame.sprite.Group()
LOST = 0
counter = 0


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_menu():
    intro_text = ["Классические гонки",
                  "Управление через стрелки влево и вправо",
                  "Игра со временем ускоряется",
                  "Нажми любую кнопку, чтобы продолжить"]

    background = pygame.transform.scale(load_image('background.png'), size)
    screen.blit(background, (0, 0))

    # Title
    font = pygame.font.Font(None, 50)

    title = font.render("Гонки", True, pygame.Color("white"))
    title_rect = title.get_rect()
    title_rect.centerx = width // 2
    title_rect.top = 50
    rect = pygame.Rect((0, 0), (150, 50))
    rect.centerx = width // 2
    rect.centery = title_rect.centery
    pygame.draw.rect(screen, pygame.Color("black"), rect)
    screen.blit(title, title_rect)

    # Rules
    text_coord = 380
    rect = pygame.Rect((0, 0), (400, 130))
    rect.centerx = width // 2
    rect.top = 375
    pygame.draw.rect(screen, pygame.Color("black"), rect)
    font = pygame.font.Font(None, 24)
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main()
        pygame.display.flip()
        clock.tick(FPS)


class Player(pygame.sprite.Sprite):
    _temp = load_image("car1.png").get_rect()
    image = pygame.transform.scale(load_image("car1.png"), (_temp.w * 0.8, _temp.h * 0.8))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.location = 0
        self.move_left()
        self.rect.bottom = 580

    def update(self, *args):
        global LOST

        if pygame.sprite.spritecollideany(self, enemy_group):
            LOST = 1

        if args:
            if args[0].type == pygame.KEYDOWN:
                if args[0].key == pygame.K_LEFT:
                    self.move_left()
                if args[0].key == pygame.K_RIGHT:
                    self.move_right()

    def move_left(self):
        self.location -= 1
        if self.location < 0:
            self.location = 0
        self.rect.left = 80 + self.location * 61

    def move_right(self):
        self.location += 1
        if self.location > 3:
            self.location = 3
        self.rect.left = 80 + self.location * 61


class Background(pygame.sprite.Sprite):
    image = load_image("background.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Background.image, size)
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect = self.rect.move(0, SPEED)
        if self.rect.top >= height:
            self.rect.bottom = 0


class Enemy(pygame.sprite.Sprite):
    _temp = load_image("car2.png").get_rect()
    image = pygame.transform.scale(load_image("car2.png"), (_temp.w * 0.8, _temp.h * 0.8))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.location = 0
        self.rect.bottom = 550
        self.spawn()

    def spawn(self):
        self.location = random.randrange(0, 4)
        self.rect.left = 79 + self.location * 60
        self.rect.bottom = -random.randrange(0, 500)
        _temp = pygame.sprite.spritecollide(self, enemy_group, False)
        _temp.remove(self)
        while _temp:
            self.location = random.randrange(0, 3)
            self.rect.left = 79 + self.location * 60
            self.rect.bottom = -random.randrange(0, 500)
            _temp = pygame.sprite.spritecollide(self, enemy_group, False)
            _temp.remove(self)

    def update(self):
        self.rect = self.rect.move(0, SPEED)
        if self.rect.top >= height:
            self.spawn()


def main():
    global SPEED, counter, enemy_group

    speed_c = 0
    counter = 0
    SPEED = 4

    sprite_group = pygame.sprite.Group()
    background_group = pygame.sprite.Group()
    background = Background(background_group)
    background2 = Background(background_group)
    background2.rect.bottom = 0
    player = Player(sprite_group)

    enemies_count = 3

    enemy_group = pygame.sprite.Group()
    for i in range(enemies_count):
        enemy = Enemy(enemy_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            sprite_group.update(event)
        sprite_group.update()

        if LOST == 1:
            end_menu()

        counter += 1
        speed_c += 1
        if speed_c == 400:
            speed_c = 0
            SPEED += 2
        background_group.update()
        enemy_group.update()
        background_group.draw(screen)
        enemy_group.draw(screen)
        sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def end_menu():
    global LOST

    intro_text = ["Игра закончена",
                  "",
                  "Нажми любую кнопку, чтобы начать заново"]

    background = pygame.transform.scale(load_image('background.png'), size)
    screen.blit(background, (0, 0))

    fo = open("highscore.txt", "a+")
    fo.close()
    fo = open("highscore.txt", "r")
    content = fo.readline()
    fo.close()
    score = 0
    if content:
        score = int(content)

    # Title
    font = pygame.font.Font(None, 50)

    title = font.render(f"Ваш счет: {counter}", True, pygame.Color("white"))
    title_rect = title.get_rect()
    title_rect.centerx = width // 2
    title_rect.top = 50

    last = font.render(f"Рекорд: {score}", True, pygame.Color("white"))
    last_rect = last.get_rect()
    last_rect.centerx = width // 2
    last_rect.top = 90

    rect = pygame.Rect((0, 0), (400, 100))
    rect.centerx = width // 2
    rect.top = 35
    pygame.draw.rect(screen, pygame.Color("black"), rect)
    screen.blit(title, title_rect)
    screen.blit(last, last_rect)

    if score < counter:
        fo = open("highscore.txt", "w")
        fo.write(str(counter))
        fo.close()

    # Rules
    text_coord = 380
    rect = pygame.Rect((0, 0), (400, 100))
    rect.centerx = width // 2
    rect.top = 375
    pygame.draw.rect(screen, pygame.Color("black"), rect)
    font = pygame.font.Font(None, 24)
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                LOST = 0

                main()
        pygame.display.flip()
        clock.tick(FPS)


start_menu()