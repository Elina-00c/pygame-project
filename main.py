import pygame

pygame.init()
surface = pygame.display.set_mode((650, 380))
pygame.display.set_caption('our game')
icone = pygame.image.load('files/icon.png')
pygame.display.set_icon(icone)

background = pygame.image.load('files/our bag.jpg')
sound = pygame.mixer.Sound('files/music.mp3')
sound.play()


class Player(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = [player_x, player_y]
        self.player_anim_count = 0
        self.walk_right = [pygame.image.load('files/player_walk/img1.png'),
                           pygame.image.load('files/player_walk/img2.png'),
                           pygame.image.load('files/player_walk/img3.png'),
                           pygame.image.load('files/player_walk/img4.png'),
                           pygame.image.load('files/player_walk/img5.png'),
                           pygame.image.load('files/player_walk/img6.png'),
                           pygame.image.load('files/player_walk/img7.png'),
                           pygame.image.load('files/player_walk/img8.png')]

        for i in range(len(self.walk_right)):
            self.walk_right[i] = pygame.transform.scale(self.walk_right[i], (int(self.walk_right[i].get_width() * size),
                                                                             int(self.walk_right[
                                                                                     i].get_height() * size)))

    def draw(self):
        surface.blit(self.walk_right[self.player_anim_count], self.rect)


player = Player(50, 237, 0.2)

speed = 8
jump = False
jump_count = 10
clock = pygame.time.Clock()

running = True
flag = True
while running:
    clock.tick(30)
    surface.blit(background, (0, 0))
    pygame.display.update()

    if flag:
        surface.blit(player.walk_right[0], player.rect)

    if player.rect[0] <= 0:
        player.rect[0] = 650
    elif player.rect[0] >= 650:
        player.rect[0] = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        flag = False
        player.draw()
        if player.player_anim_count == 7:
            player.player_anim_count = 0
        else:
            player.player_anim_count += 1
        player.rect[0] -= speed
    elif keys[pygame.K_RIGHT]:
        flag = False
        player.draw()
        if player.player_anim_count == 7:
            player.player_anim_count = 0
        else:
            player.player_anim_count += 1
        player.rect[0] += speed
    else:
        flag = True

    if not jump:
        if keys[pygame.K_UP]:
            jump = True
    else:
        if jump_count >= -10:
            if jump_count > 0:
                player.rect[1] -= (jump_count ** 2) / 2
            else:
                player.rect[1] += (jump_count ** 2) / 2
            jump_count -= 1
        else:
            jump = False
            jump_count = 10

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
