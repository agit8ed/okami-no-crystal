import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(70, 70)

FPS = 50
WIDTH = 800
HEIGHT = 600
STEP = 20

STANDING = 0
# MOVING = 1
JUMPING = 2
FALLING = 3
FALLING_AFTER_JUMP = 4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

global_death_flag = False
startup_flag = True

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
projectiles_group = pygame.sprite.Group()
spells_group = pygame.sprite.Group()
sword_group = pygame.sprite.Group()
wall_tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
start_text_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()

tileset = []


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    global tileset
    new_player, new_player_2, new_player_2_flip, new_enemy, x, y = None, None, None, None, None, None
    tileset = []
    print(level)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'n':
                extra_tile = Tile('empty', x, y)
                tileset.append(extra_tile)
            elif level[y][x] == 'f':
                extra_tile = FloorTile('wall', x, y)
                tileset.append(extra_tile)
                # Tile('wall', x, y)
            elif level[y][x] == "s":
                extra_tile = Tile("sky", x, y)
                tileset.append(extra_tile)
            elif level[y][x] == 'p':
                extra_tile = Tile("sky", x, y)
                new_player = Player(x, y)
                print(x, y)
                SpeechBubble(x, y - 100)
                tileset.append(extra_tile)
            elif level[y][x] == 'a':
                extra_tile = Tile("sky", x, y)
                new_player_2 = AnimatedPlayer(load_image("hoodguy_animated_tailfull.png"), 6, 2, 92, 95)
                new_player_2_flip = AnimatedPlayer(load_image("hoodguy_animated_tailfull_flip.png"), 6, 2, 92, 95)
                tileset.append(extra_tile)
            elif level[y][x] == "e":
                extra_tile = Tile("sky", x, y)
                new_enemy = Enemy(x, y)
                tileset.append(extra_tile)
    print(new_player.rect.x, new_player.rect.y)
    return [new_player, new_player_2, new_player_2_flip, new_enemy, x, y]


def reload_level(level):
    global player, player_2, player_2_flip, current_enemy, level_x, level_y
    global current_level
    global healthbar, redhealth, greenmana
    for i in all_sprites:
        print(i)
        i.kill()
        del i
    for i in range(len(level)):
        level[i] = None
    current_level = player, player_2, player_2_flip, current_enemy, level_x, level_y = \
        generate_level(load_level(current_level_name))
    healthbar, redhealth, greenmana = HealthBar(health_sprites[0], 0, 0), HealthBar(health_sprites[1], 193, 81), \
    HealthBar(health_sprites[2], 193, 75)


def terminate():
    pygame.quit()
    sys.exit()


def exists_as_a_link_to_main():
    return


def draw_sprites():
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    wall_tiles_group.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    projectiles_group.draw(screen)
    spells_group.draw(screen)
    sword_group.draw(screen)
    health_group.draw(screen)
    end_group.draw(screen)


def gameover():
    global global_death_flag
    global redhealth
    overgame = pygame.transform.scale(load_image('gameover.png'), (WIDTH, HEIGHT))
    screen.blit(overgame, (0, 0))
    '''global current_level
    global player
    global player_2
    global player_2_flip
    global current_enemy
    global level_x
    global level_y'''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                global_death_flag = False
                player.death_flag = False
                player.hit_points = 4
                redhealth.image = load_image("red_health.png")
                start_screen()
                reload_level(current_level)
                return
        pygame.display.flip()
        clock.tick(FPS)


def options():
    global startup_flag
    intro_text = ["start", "continue", "options"]
    warning_text = "THIS IS MEANT TO BE AN OPTIONS SCREEN"
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color("white"))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    text_warning = font.render(warning_text, 1, pygame.Color("white"))
    warning_rect = text_warning.get_rect()
    warning_rect.top = 400
    warning_rect.x = 200
    screen.blit(text_warning, warning_rect)

    while True:
        # print("0")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # print("1")
                startup_flag = False
                return
            '''elif event.type or event.type == pygame.NOEVENT:
                if running_timer % 15 == 0:
                    print("it works")
                    start_text = load_image("press_start_flash.png")
                    screen.blit(start_text, (WIDTH - 720, HEIGHT - 110))
                else:
                    start_text = load_image("press_start.png")
                    screen.blit(start_text, (WIDTH - 720, HEIGHT - 110))'''
        pygame.display.flip()
        clock.tick(FPS)
        # print("2")


def start_screen():
    global startup_flag
    running_timer = 0

    title = pygame.transform.scale(load_image('okami_no_crystal.jpg'), (WIDTH, HEIGHT))
    start_text = StartText(WIDTH - 720, HEIGHT - 110)
    screen.blit(title, (0, 0))

    '''font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)'''
    while True:
        running_timer += 1
        # print("0")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # print("1")
                start_text_group.remove(start_text)
                startup_flag = False
                options()
                return
            '''elif event.type or event.type == pygame.NOEVENT:
                if running_timer % 15 == 0:
                    print("it works")
                    start_text = load_image("press_start_flash.png")
                    screen.blit(start_text, (WIDTH - 720, HEIGHT - 110))
                else:
                    start_text = load_image("press_start.png")
                    screen.blit(start_text, (WIDTH - 720, HEIGHT - 110))'''

        start_text_group.draw(screen)
        start_text.update()
        pygame.display.flip()
        clock.tick(FPS)
        # print("2")


class StartText(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, start_text_group)
        self.image = load_image("press_start.png")
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.text_timer = 0

    def update(self):
        self.text_timer += 1
        if self.text_timer == 50:
            self.image = load_image("press_start_flash.png")
        if self.text_timer == 100:
            self.image = load_image("press_start.png")
            self.text_timer = 0


'''class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]'''


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class FloorTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(wall_tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class SpeechBubble(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = load_image("dotdotdot.png")
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        print("Nani?!")


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        global global_mana_points
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.image_for_invin = player_image
        self.states = (STANDING, JUMPING, FALLING)  # for reference
        self.current_state = FALLING
        self.jump_timer = 0
        self.jump_flag = False  # flag for executing a jump
        self.jumped_flag = False  # flag for after a jump has been completed
        self.jump_count = 1
        self.hit_points = 4
        self.mana_points = global_mana_points = 4
        self.spell_flag = False
        self.cooldown = 50
        self.mana_point_timer = 60
        self.death_flag = False
        self.invincible_flag = False
        self.invincible_timer = 0
        self.collision_flag = False
        # self.prev_height = 0
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def state_control(self):
        global greenmana
        global global_mana_points
        # print(self.current_state, "it me")
        if self.current_state == JUMPING and self.jump_flag is True:
            self.jump_timer += 1
            # print(self.jump_timer)
            self.rect.y -= 10
            if moving_flag is True:
                if left_flag is False:
                    self.rect.x += 10
                else:
                    self.rect.x -= 10
            if self.jump_timer == 20:
                self.jump_timer = 0
                self.jump_flag = False
                self.jumped_flag = True
                self.current_state = FALLING_AFTER_JUMP
        elif self.current_state == FALLING_AFTER_JUMP:
            self.rect.y += 10
            if moving_flag is True:
                if left_flag is False:
                    self.rect.x += 10
                else:
                    self.rect.x -= 10
        elif self.current_state == FALLING and self.jump_flag is False:
            self.rect.y += 10
        elif self.current_state == STANDING:
            self.jump_count = 1
            if self.mana_points == 4:
                greenmana.image = load_image("green_mana.png")
            if self.mana_points < 4 and self.spell_flag is False:
                self.mana_point_timer -= 1
                if self.mana_point_timer == 0 and self.mana_points < 4:
                    self.mana_points += 1
                    self.mana_point_timer = 60
                for i in range(len(green_mana_sprites)):
                    try:
                        greenmana.image = green_mana_sprites[3 - player.mana_points]
                        global_mana_points = self.mana_points
                        print(self.mana_points)
                    except IndexError:
                        greenmana.image = load_image("depleted.png")
            if self.spell_flag is True:
                self.cooldown -= 1
                # print(self.cooldown, "it flag")
                if self.cooldown == 0:
                    self.spell_flag = False
                    self.cooldown = 50

    def death(self):
        global global_death_flag
        global overgame
        self.death_flag = True
        global_death_flag = True
        GameOver()

    def update(self):
        self.state_control()
        if pygame.sprite.spritecollideany(self, wall_tiles_group) is not None and self.jump_flag is False:
            # self.prev_height = self.rect.top
            self.current_state = STANDING
            self.moving_flag = False
            self.jumped_flag = False
        if pygame.sprite.spritecollideany(self, wall_tiles_group) is None and self.jump_flag is False:
            if self.jumped_flag is True:
                self.current_state = FALLING_AFTER_JUMP
            else:
                self.current_state = FALLING
        if pygame.sprite.spritecollideany(self, projectiles_group) is not None \
                or pygame.sprite.spritecollideany(self, enemy_group) is not None:
            # print(self.invincible_flag)
            if self.invincible_flag is False:
                self.hit_points -= 1
                try:
                    for i in range(len(red_health_sprites)):
                        redhealth.image = red_health_sprites[3 - self.hit_points]
                except IndexError:
                    redhealth.image = load_image("depleted.png")
                self.invincible_flag = True
        elif self.invincible_flag is True:
            self.invincible_timer += 1
            # print(self.invincible_timer)
            if self.invincible_timer % 5 == 0:
                self.image = load_image("invuln_flash.png")
            else:
                # print(self.image_for_invin)
                self.image = self.image_for_invin
            if self.invincible_timer == 150:
                self.invincible_flag = False
                self.image = self.image_for_invin
                self.invincible_timer = 0
        if self.hit_points <= 0:
            self.death()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.fire_flag = True
        self.fire_timer = 0
        self.movement_timer = 0

    def enemy_ai(self):
        self.movement_timer += 1
        self.fire_timer += 1
        if self.movement_timer < 20:
            self.rect.x += 5
        elif 20 < self.movement_timer < 41:
            self.rect.x -= 5
        elif self.movement_timer == 41:
            self.movement_timer = 0
        if self.fire_timer == 50 and self.fire_flag is True:
            EnemyProjectile(self.rect.x, self.rect.y + 25, -5, 0)
            self.fire_timer = 0

    def update(self):
        if global_death_flag is False:
            self.enemy_ai()
            if pygame.sprite.spritecollideany(self, wall_tiles_group) is None:
                self.rect.top += 10
            if pygame.sprite.spritecollideany(self, sword_group) is not None or \
                    pygame.sprite.spritecollideany(self, spells_group) is not None:
                self.fire_timer = 0
                self.fire_flag = False
                self.movement_timer = 0
                enemy_group.remove(self)


class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, end_group)
        self.image = load_image("depleted.png")
        self.rect = self.image.get_rect().move(0, 0)

    def update(self):
        if global_death_flag is True:
            gameover()
        else:
            end_group.remove(self)


class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, x_d, y_d):
        super().__init__(projectiles_group, all_sprites)
        self.image = load_image("snake_fireball_flip.png")
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.projectile_timer = 0
        self.x_d = x_d
        self.y_d = y_d

    def update(self):
        if global_death_flag is False:
            self.projectile_timer += 1
            # print("Where though?")
            if pygame.sprite.spritecollideany(self, player_group) is None:
                self.rect.x += self.x_d
                self.rect.y += self.y_d
            if pygame.sprite.spritecollideany(self, player_group) is not None \
                    or pygame.sprite.spritecollideany(self, sword_group) is not None \
                    or pygame.sprite.spritecollideany(self, spells_group) is not None:
                projectiles_group.remove(self)
            if self.projectile_timer == 500:
                projectiles_group.remove(self)
                self.projectile_timer = 0


class FriendlyProjectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, x_d, y_d, spell_image):
        super().__init__(spells_group, all_sprites)
        self.image = spell_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.spell_timer = 0
        self.x_d = x_d
        self.y_d = y_d

    def update(self):
        if global_death_flag is False:
            self.spell_timer += 1
            # print("Where though?")
            if pygame.sprite.spritecollideany(self, projectiles_group) is None and \
                    pygame.sprite.spritecollideany(self, enemy_group) is None:
                self.rect.x += self.x_d
                self.rect.y += self.y_d
            if pygame.sprite.spritecollideany(self, enemy_group) is not None \
                    or pygame.sprite.spritecollideany(self, projectiles_group) is not None:
                spells_group.remove(self)
            if self.spell_timer == 500:
                spells_group.remove(self)
                self.spell_timer = 0


class AnimatedPlayer(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, player_group)
        self.collision_flag = False
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if pygame.sprite.spritecollideany(self, wall_tiles_group) is None:
            self.rect.top += 10


class SwordSlash(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sword_image):
        super().__init__(sword_group, all_sprites)
        self.image = sword_image
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.sword_timer = 0

    def update(self):
        self.sword_timer += 1
        self.rect = self.image.get_rect().move(self.pos)
        '''if pygame.sprite.spritecollideany(self, enemy_group) is not None:
            sword_group.remove(self)
        if pygame.sprite.spritecollideany(self, projectiles_group) is not None:
            sword_group.remove(self)'''
        if self.sword_timer == 10:
            sword_group.remove(self)
            self.sword_timer = 0


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(health_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx
        '''if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])'''
        obj.rect.y += self.dy
        '''if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])'''

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


tile_images = {'wall': load_image('normal_tile.png'), 'empty': load_image('ruby_tile.png'),
               "sky": load_image("sky_tile.png")}
player_image = load_image('hoodguy_field_s_bw.png')
player_2_image = load_image("hoodguy_animated_4.png")
enemy_image = load_image("super_small_snake_flip.png")

tile_width = tile_height = 200

global_mana_points = 0

overgame = None

health_sprites = (load_image("health_and_mana.png"), load_image("red_health.png"), load_image("green_mana.png"))
red_health_sprites = \
    (load_image("red_health_three.png"), load_image("red_health_two.png"), load_image("red_health_one.png"))
green_mana_sprites = (load_image("green_mana_three.png"), load_image("green_mana_two.png"),
                      load_image("green_mana_one.png"))
healthbar, redhealth, greenmana = HealthBar(health_sprites[0], 0, 0), HealthBar(health_sprites[1], 193, 81), \
                                  HealthBar(health_sprites[2], 193, 75)
left_flag = False
moving_flag = False
current_level_name = "levely.txt"
current_level = [player, player_2, player_2_flip, current_enemy, level_x, level_y] = \
    generate_level(load_level(current_level_name))
sword_image = (load_image("sword_slash.png"), load_image("sword_slash_flip.png"))
spell_image = (load_image("spear.png"), load_image("spear_flip.png"))

if startup_flag is True:
    start_screen()


def main():
    print("START!")
    global player
    global left_flag
    global greenmana
    global global_mana_points
    global moving_flag

    camera = Camera((level_x, level_y))
    running_timer = 0

    running = True
    while running:
        running_timer += 1
        if startup_flag is True:
            start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type or event.type == pygame.NOEVENT:
                moving_flag = False
                if player.death_flag is False:
                    if running_timer % 15 == 0:
                        if left_flag is False:
                            player.image = load_image("hoodguy_field_tail_s_bw.png")
                        else:
                            player.image = load_image("hoodguy_field_tail_flip_s_bw.png")
                    else:
                        if left_flag is False:
                            player.image = load_image("hoodguy_field_s_bw.png")
                        else:
                            player.image = load_image("hoodguy_field_flip_s_bw.png")
            # elif event.type == pygame.KEYDOWN:
            if player.death_flag is False:
                if pygame.key.get_pressed()[pygame.K_LEFT] == 1 or pygame.key.get_pressed()[pygame.K_a] == 1:
                    '''if player.jump_flag is True:
                        player.current_state = MOVING_IN_THE_AIR_UP
                    elif player.current_state == STANDING:
                        player.current_state = MOVING
                    else:
                        player.current_state = MOVING_IN_THE_AIR_DOWN'''
                    # player.current_state = MOVING
                    moving_flag = True
                    left_flag = True
                    player.rect.x -= STEP
                    # player_2_flip.rect.x -= STEP
                    if player.invincible_flag is True:
                        player.image_for_invin = load_image("hoodguy_field_flip_s_bw.png")
                        if running_timer % 15 == 0:
                            player.image_for_invin = load_image("hoodguy_field_tail_flip_s_bw.png")
                    else:
                        player.image = player.image_for_invin = load_image("hoodguy_field_flip_s_bw.png")
                        if running_timer % 15 == 0:
                            player.image = player.image_for_invin = load_image("hoodguy_field_tail_flip_s_bw.png")
                if pygame.key.get_pressed()[pygame.K_RIGHT] == 1 or pygame.key.get_pressed()[pygame.K_d] == 1:
                    '''if player.jump_flag is True:
                        player.current_state = MOVING_IN_THE_AIR_UP
                    elif player.current_state == STANDING:
                        player.current_state = MOVING
                    else:
                        player.current_state = MOVING_IN_THE_AIR_DOWN'''
                    # player.current_state = MOVING
                    left_flag = False
                    moving_flag = True
                    player.rect.x += STEP
                    # player_2.rect.x += STEP
                    if player.invincible_flag is True:
                        player.image_for_invin = load_image("hoodguy_field_s_bw.png")
                        if running_timer % 15 == 0:
                            player.image_for_invin = load_image("hoodguy_field_tail_s_bw.png")
                    else:
                        player.image = player.image_for_invin = load_image("hoodguy_field_s_bw.png")
                        if running_timer % 15 == 0:
                            player.image = player.image_for_invin = load_image("hoodguy_field_tail_s_bw.png")
                if pygame.key.get_pressed()[pygame.K_p] == 1:
                    if left_flag is True:
                        SwordSlash(player.rect.x - 50, player.rect.y - 15, sword_image[1])
                    else:
                        SwordSlash(player.rect.x, player.rect.y - 15, sword_image[0])
                if pygame.key.get_pressed()[pygame.K_l] == 1:
                    if player.mana_points > 0 and player.spell_flag is False:
                        if left_flag is True:
                            FriendlyProjectile(player.rect.x - 50, player.rect.y - 15, -10, 0, spell_image[1])
                        else:
                            FriendlyProjectile(player.rect.x, player.rect.y - 15, 10, 0, spell_image[0])
                        player.mana_points -= 1
                        player.spell_flag = True
                        global_mana_points = player.mana_points
                    else:
                        pass
                if pygame.key.get_pressed()[pygame.K_SPACE] == 1:
                    if player.jump_flag is False and player.jump_timer == 0 and player.jump_count == 1:
                        player.current_state = JUMPING
                        player.jump_flag = True
                        player.jump_count -= 1
                    else:
                        pass
            else:
                gameover()

        camera.update(player)

        for sprite in all_sprites:
            if sprite is not healthbar and sprite is not redhealth and sprite is not greenmana:
                camera.apply(sprite)

        screen.fill(pygame.Color("black"))
        draw_sprites()
        all_sprites.update()
        player_group.update()
        enemy_group.update()
        projectiles_group.update()

        pygame.display.flip()

        clock.tick(FPS)

    terminate()


if __name__ == "__main__":
    main()
