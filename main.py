import pygame
import random

pygame.init()
surface = pygame.display.set_mode((650, 380))
pygame.display.set_caption('our game')

icone = pygame.image.load('files/icon.png')
pygame.display.set_icon(icone)

background = pygame.image.load('files/our bag.jpg')
sound = pygame.mixer.Sound('files/music.mp3')
# sound.play(-1)
start_game = False

level = 1
rows = 2
cols = 7
title_size = 650 // rows


class Button:
    window_size = (650, 380)
    screen = pygame.display.set_mode(window_size)

    # Создаем объект шрифта
    font = pygame.font.Font(None, 24)

    # Создайте поверхность для кнопки
    button_surface = pygame.Surface((150, 50))

    # Отображение текста на кнопке
    text = font.render("Start", True, (0, 0, 0))
    text_rect = text.get_rect(
        center=(button_surface.get_width() / 2,
                button_surface.get_height() / 2))

    # Создайте объект pygame.Rect, который представляет границы кнопки
    button_rect = pygame.Rect(125, 125, 150, 50)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, size):
        pygame.sprite.Sprite.__init__(self)
        self.move_right = False
        self.alive = True
        self.move_left = False
        self.flag_jump = False
        self.direction = 1
        self.flip = False
        self.jump_count = 10
        self.rect = [player_x, player_y]
        self.player_anim_count = 0
        self.speed = 8
        self.walk_right = []
        self.flag_move = False
        self.player_anim_count_attac = 0
        self.update_time = pygame.time.get_ticks()
        self.attac = []
        self.flag_attac = False
        for i in range(1, 3):
            img = pygame.image.load(f'files/walk_right/img{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * size), int(img.get_height() * size)))
            self.walk_right.append(img)
        for i in range(1, 2):
            img = pygame.image.load(f'files/attac/img{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * size), int(img.get_height() * size)))
            self.attac.append(img)

    def draw(self):
        surface.blit(pygame.transform.flip(self.walk_right[self.player_anim_count], self.flip, False), self.rect)

    def animation(self):
        animation_clock = 100
        if pygame.time.get_ticks() - self.update_time > animation_clock and self.flag_move:
            self.update_time = pygame.time.get_ticks()
            self.player_anim_count += 1
        if self.player_anim_count == len(self.walk_right):
            self.player_anim_count = 0

    def move(self):
        if self.move_right:
            self.rect[0] += self.speed
            self.move_right = False
            self.flip = False
            self.direction = -1
        elif self.move_left:
            self.rect[0] -= self.speed
            self.move_left = False
            self.flip = True
            self.direction = 1

    def jumper(self):
        if self.jump_count >= -10:
            if self.jump_count > 0:
                self.rect[1] -= (self.jump_count ** 2) / 2
            else:
                self.rect[1] += (self.jump_count ** 2) / 2
            self.jump_count -= 1
        else:
            self.flag_jump = False
            self.jump_count = 10

    def attac_animation(self):
        animation_clock = 100
        if pygame.time.get_ticks() - self.update_time > animation_clock:
            self.update_time = pygame.time.get_ticks()
            self.player_anim_count_attac = 0
        self.draw_attac()

    def draw_attac(self):
        surface.blit(pygame.transform.flip(self.attac[self.player_anim_count_attac], self.flip, False), self.rect)
        self.flag_attac = False

    def shoot(self):
        pass

    def check_live(self):
        pass

    def restart(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_x, enemy_y, size):
        pygame.sprite.Sprite.__init__(self)
        self.animation = []
        self.enemy_rect = [enemy_x, enemy_y]
        self.update_time = pygame.time.get_ticks()
        self.enemy_anim_count = 0
        for i in range(1, 10):
            img = pygame.image.load(f'files/enemy/img{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * size), int(img.get_height() * size)))
            self.animation.append(img)

    def draw_enemy(self):
        surface.blit(self.animation[self.enemy_anim_count], self.enemy_rect)

    def animation_enemy(self):
        animation_clock = 100
        if pygame.time.get_ticks() - self.update_time > animation_clock:
            self.update_time = pygame.time.get_ticks()
            self.enemy_anim_count += 1
        if self.enemy_anim_count == len(self.animation):
            self.enemy_anim_count = 0


class Bullet(pygame.sprite.Sprite):
    def init(self, x, y):
        pygame.sprite.Sprite.init(self)

    def func(self):
        pass


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health / self.max_health
        # pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        # pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        # pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class Exit:
    pass


class Title:
    pass


class Level:
    pass


class Barrier:
    pass


player = Player(0, 160, 0.2)
button = Button()
enemy = Enemy(300, 175, 0.2)

clock = pygame.time.Clock()

running = True
flag = True
while running:
    clock.tick(30)
    # start window
    if not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Вызовите функцию on_mouse_button_down()
                if button.button_rect.collidepoint(event.pos):
                    start_game = True
        if button.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button.button_surface, (127, 255, 212), (1, 1, 148, 48))
        else:
            pygame.draw.rect(button.button_surface, (0, 0, 0), (0, 0, 150, 50))
            pygame.draw.rect(button.button_surface, (255, 255, 255), (1, 1, 148, 48))
            pygame.draw.rect(button.button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
            pygame.draw.rect(button.button_surface, (0, 100, 0), (1, 48, 148, 10), 2)

        button.button_surface.blit(button.text, button.text_rect)
        button.screen.blit(button.button_surface, (button.button_rect.x, button.button_rect.y))
        pygame.display.update()
    # start window
    else:
        surface.blit(background, (0, 0))
        player.animation()
        enemy.draw_enemy()
        if abs(player.rect[0] - enemy.enemy_rect[0]) < 200:
            enemy.animation_enemy()
        else:
            enemy.enemy_anim_count = 0
        player.flag_move = False

        keys = pygame.key.get_pressed()
        player.draw()
        if keys[pygame.K_LEFT]:
            player.move_left = True
            player.flag_move = True
            player.move()
        if keys[pygame.K_RIGHT]:
            player.flag_move = True
            player.move_right = True
            player.move()
        if keys[pygame.K_w]:
            player.flag_attac = True
            player.attac_animation()

        if not player.flag_jump:
            if keys[pygame.K_UP]:
                player.flag_jump = True
        else:
            player.jumper()

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pass

while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
