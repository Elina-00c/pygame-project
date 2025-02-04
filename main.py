import pygame
from pyvidplayer2 import Video
import random

pygame.init()
wight = 830
height = 500
surface = pygame.display.set_mode((wight, height))
pygame.display.set_caption('our game')

icone = pygame.image.load('files/icon.png')
pygame.display.set_icon(icone)

background_level1 = pygame.image.load('files/background1.png')
background_level2 = pygame.image.load('files/back.jpg')
current_background = background_level1

sound = pygame.mixer.Sound('files/music.mp3')
sound.play(-1)

dead_img = pygame.image.load('files/dead.png')
dead_img = pygame.transform.scale(dead_img, (int(dead_img.get_width() * 0.1), int(dead_img.get_height() * 0.1)))

coin_image = pygame.image.load('files/coins.png')
coin_image = pygame.transform.scale(coin_image, (int(coin_image.get_width() * 2), int(coin_image.get_height() * 2)))

start_game = False

# vid = Video('files/video.mp4')
win = pygame.display.set_mode((1280, 720))

tile_size = 30
game_over = False

coin_counter = 0
current_level = 1

level1_data = [
    [0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0],
    [3, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 3],
    [0, 0, 1, 0, 1, 3, 0, 1, 0, 3, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 2, 1, 0, 1, 2, 2, 1, 0, 1, 2, 2, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

level2_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 3, 0, 0, 3, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

class World:
    def __init__(self, data):
        grass_image = pygame.image.load('files/gress.jpg')
        water_image = pygame.image.load('files/water.png')
        coin_image = pygame.image.load('files/coin.png')

        self.tile_list = []
        self.coins = []
        self.coin_positions = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # Обычный блок
                    img = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 2:  # Вода
                    img = pygame.transform.scale(water_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 3:  # Монеты
                    img_rect = pygame.Rect(col_count * tile_size + tile_size // 4,
                                           row_count * tile_size + tile_size // 4,
                                           tile_size // 2, tile_size // 2)
                    self.coins.append(img_rect)
                    self.coin_positions.append(img_rect.copy())  # Сохраняем копию позиции

                def reset_coins(self):
                    """Восстанавливаем монеты при рестарте"""
                    self.coins = [coin.copy() for coin in self.coin_positions]

                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            surface.blit(tile[0], tile[1])
            # pygame.draw.rect(surface, (255, 255, 255), tile[1], 2)


word_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

coin_image = pygame.image.load('files/coin.png')
coin_width, coin_height = coin_image.get_size()
coins = []
for y, row in enumerate(word_data):
    for x, cell in enumerate(row):
        if cell == 3:
            coins.append(pygame.Rect(x * tile_size, y * tile_size, coin_width, coin_height))


world = World(word_data)


class Button:
    window_size = (827, 500)
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
        self.walk_right = []
        self.coin_count = 0
        self.player_start_x = player_x
        self.player_start_y = player_y
        self.walk_left = []
        self.player_anim_count = 0
        self.count = 0
        for i in range(1, 5):
            img_right = pygame.image.load(f'files/player_walk/guy{i}.png')
            img_right = pygame.transform.scale(img_right,
                                               (int(img_right.get_width() * size), int(img_right.get_height() * size)))
            img_left = pygame.transform.flip(img_right, True, False)
            self.walk_right.append(img_right)
            self.walk_left.append(img_left)
        self.image = self.walk_right[self.player_anim_count]
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def move(self, world):
        dx = 0
        dy = 0
        walk_cooldown = 5

        key = pygame.key.get_pressed()

        if key[pygame.K_q]:
            self.restart_game(world)

        # Проверка, если персонаж на земле
        on_ground = False
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + 1, self.width, self.height):
                on_ground = True

        # Прыжок только если персонаж на земле
        if key[pygame.K_SPACE] and on_ground and not self.jumped:
            self.vel_y = -12
            self.jumped = True

        if not key[pygame.K_SPACE]:
            self.jumped = False

        if key[pygame.K_LEFT]:
            dx -= 3.5
            self.count += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 3.5
            self.count += 1
            self.direction = 1
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.count = 0
            self.player_anim_count = 0
            if self.direction == 1:
                self.image = self.walk_right[self.player_anim_count]
            if self.direction == -1:
                self.image = self.walk_left[self.player_anim_count]

        if self.count > walk_cooldown:
            self.count = 0
            self.player_anim_count += 1
            if self.player_anim_count >= len(self.walk_right):
                self.player_anim_count = 0
            if self.direction == 1:
                self.image = self.walk_right[self.player_anim_count]
            if self.direction == -1:
                self.image = self.walk_left[self.player_anim_count]

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

        self.collect_coins(world)

        surface.blit(self.image, self.rect)

    def collect_coins(self, world):
        """Проверяем столкновение с монетами и удаляем их при сборе"""
        for coin in world.coins[:]:  # Перебираем копию списка, чтобы удалять
            if self.rect.colliderect(coin):
                world.coins.remove(coin)
                self.coin_count += 1

    def restart_game(self, world):
        """Перезапуск игры: сбрасываем монеты и счет"""
        self.rect.x, self.rect.y = 100, 100
        self.vel_y = 0
        self.jumped = False
        self.coin_count = 0

        # Восстанавливаем монеты
        world.reset_coins()

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
        self.image = self.animation[self.enemy_anim_count]
        self.rect = self.image.get_rect()

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


player = Player(0, 160, 0.4)
button = Button()
enemy_list = []
enemy = Enemy(270, 375, 0.15)
enemy_list.append(enemy.enemy_rect)
enemy1 = Enemy(349, 230, 0.15)
enemy_list.append(enemy1.enemy_rect)
enemy2 = Enemy(349, 145, 0.15)
enemy_list.append(enemy2.enemy_rect)

clock = pygame.time.Clock()

running = True
flag = True
while running:
    clock.tick(90)
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Coins: {player.coin_count}", True, (255, 255, 255))
    surface.blit(score_text, (10, 10))  # Отображаем счет в левом верхнем углу
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

        clock.tick(60)

        surface.blit(background, (0, 0))

        world.draw()

        player.move(world)
        enemy.draw_enemy()
        enemy1.draw_enemy()
        enemy2.draw_enemy()
        enemy.animation_enemy()
        enemy1.animation_enemy()
        if abs(enemy.enemy_rect[0] - 9 - player.rect.x < 15) and abs(enemy.enemy_rect[1] + 285 - player.rect.y < 15):
            surface.blit(dead_img, (player.rect.x, player.rect.y))
        if abs(enemy1.enemy_rect[0] - 9 - player.rect.x < 15) and abs(enemy1.enemy_rect[1] + 285 - player.rect.y < 15):
            surface.blit(dead_img, (player.rect.x, player.rect.y))
        if abs(enemy1.enemy_rect[0] - 9 - player.rect.x < 15) and abs(enemy1.enemy_rect[1] + 285 - player.rect.y < 15):
            surface.blit(dead_img, (player.rect.x, player.rect.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
