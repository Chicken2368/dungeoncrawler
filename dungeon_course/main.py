import pygame
import csv
import constants
from weapon import Weapon
from items import Item
from world import World


pygame.init()


class ScreenFade:
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_HEIGHT, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        elif self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))

            if self.fade_counter >= constants.SCREEN_WIDTH:
                fade_complete = True

        return fade_complete


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


def draw_text(text, font, colour, x, y):
    image = font.render(text, True, colour)
    screen.blit(image, (x, y))


def scale_image(image, w_scale, h_scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * w_scale, h * h_scale))


def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif player.health % 20 > 0 and not half_heart_drawn:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))

    draw_text(f"LEVEL: {level}", font, constants.WHITE, constants.SCREEN_WIDTH - 700, 15)
    draw_text(f":{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)


def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    data = []

    for line in range(constants.ROWS):
        tile_type = [-1] * constants.COLUMNS
        data.append(tile_type)

    return data


screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon")

clock = pygame.time.Clock()

level = 1
start_intro = True
screen_scroll = [0, 0]

moving_left = False
moving_right = False
moving_up = False
moving_down = False
sprint = False
sneak = False

font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)


bow_image = pygame.image.load("assets/images/weapons/bow.png").convert_alpha()
bow_image = scale_image(bow_image, constants.WEAPON_SCALE, constants.WEAPON_SCALE)

arrow_image = pygame.image.load("assets/images/weapons/arrow.png").convert_alpha()
arrow_image = scale_image(arrow_image, constants.WEAPON_SCALE, constants.WEAPON_SCALE)

heart_full = pygame.image.load("assets/images/items/heart_full.png").convert_alpha()
heart_full = scale_image(heart_full, constants.ITEM_SCALE, constants.ITEM_SCALE)

heart_half = pygame.image.load("assets/images/items/heart_half.png").convert_alpha()
heart_half = scale_image(heart_half, constants.ITEM_SCALE, constants.ITEM_SCALE)

heart_empty = pygame.image.load("assets/images/items/heart_empty.png").convert_alpha()
heart_empty = scale_image(heart_empty, constants.ITEM_SCALE, constants.ITEM_SCALE)
coin_images = []
for x in range(4):
    coin_image = pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha()
    coin_image = scale_image(coin_image, constants.POTION_SCALE, constants.POTION_SCALE)
    coin_images.append(coin_image)

red_potion = pygame.image.load("assets/images/items/potion_red.png").convert_alpha()
red_potion = scale_image(red_potion, constants.ITEM_SCALE, constants.ITEM_SCALE)

fireball_image = pygame.image.load("assets/images/weapons/fireball.png").convert_alpha()
fireball_image = scale_image(fireball_image, constants.FIREBALL_SCALE, constants.FIREBALL_SCALE)

item_images = [coin_images, [red_potion]]

tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)


mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "chomp_chomp"]

animation_types = ["idle", "run"]
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_image(img, constants.SCALE, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLUMNS
    world_data.append(r)

with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()

world.process_data(world_data, tile_list, item_images, mob_animations)

player = world.player
bow = Weapon(bow_image, arrow_image)


enemy_list = world.character_list


damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 110, 25, 0, coin_images, False)
for item in world.item_list:
    item_group.add(item)
item_group.add(score_coin)


intro_fade = ScreenFade(1, constants.GREY, 12)
death_fade = ScreenFade(2, constants.PINK, 12)

run = True

while run:

    clock.tick(constants.FPS)
    screen.fill(constants.BG)

    if player.alive:

        dx = 0
        dy = 0
        if moving_left:
            dx = -5
        if moving_right:
            dx = 5
        if moving_up:
            dy = -5
        if moving_down:
            dy = 5

        screen_scroll, level_complete = player.move(dx, dy, sprint, sneak, world.obstacle_tiles, world.exit_tile)
        world.update(screen_scroll)
        player.update()
        for enemy in enemy_list:
            fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
            if fireball:
                fireball_group.add(fireball)
            if enemy.alive:
                enemy.update()

        arrow = bow.update(player)
        if arrow:
            arrow_group.add(arrow)
        for arrow in arrow_group:
            damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
            if damage:
                damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                damage_text_group.add(damage_text)
        damage_text_group.update(screen_scroll)
        fireball_group.update(screen_scroll, player)
        item_group.update(screen_scroll, player)
    world.draw(screen)
    player.draw(screen)
    damage_text_group.draw(screen)
    bow.draw(screen)

    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)

    for arrow in arrow_group:
        arrow.draw(screen)

    for fireball in fireball_group:
        fireball.draw(screen)

    if level_complete:
        start_intro = True
        if level != constants.LAST_LEVEL:
            level += 1
        else:
            level = 1
        level_complete = False
        enemy_list = []
        world_data = reset_level()
        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

        world = World()
        world.process_data(world_data, tile_list, item_images, mob_animations)
        temp_hp = player.health
        temp_score = player.score
        player = world.player
        player.health = temp_hp
        player.score = temp_score
        enemy_list = world.character_list
        score_coin = Item(constants.SCREEN_WIDTH - 110, 25, 0, coin_images, False)
        item_group.add(score_coin)
        world.draw(screen)
        for item in world.item_list:
            item_group.add(item)

    if start_intro:
        if intro_fade.fade():
            start_intro = False
            intro_fade.fade_counter = 0

    if not player.alive:
        if death_fade.fade():
            death_fade.fade_counter = 0
            start_intro = True
            enemy_list = []
            world_data = reset_level()
            with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)

            world = World()
            world.process_data(world_data, tile_list, item_images, mob_animations)
            temp_score = player.score
            player = world.player
            player.health = temp_hp
            player.score = temp_score
            enemy_list = world.character_list
            score_coin = Item(constants.SCREEN_WIDTH - 110, 25, 0, coin_images, False)
            item_group.add(score_coin)
            world.draw(screen)
            for item in world.item_list:
                item_group.add(item)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True

            if event.key == pygame.K_d:
                moving_right = True

            if event.key == pygame.K_w:
                moving_up = True

            if event.key == pygame.K_s:
                moving_down = True

            if event.key == pygame.K_SPACE:
                sprint = True

            if event.key == pygame.K_LSHIFT:
                sneak = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False

            if event.key == pygame.K_d:
                moving_right = False

            if event.key == pygame.K_w:
                moving_up = False

            if event.key == pygame.K_s:
                moving_down = False

            if event.key == pygame.K_SPACE:
                sprint = False

            if event.key == pygame.K_LSHIFT:
                sneak = False

    pygame.display.update()

pygame.quit()
