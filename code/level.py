import pygame
from settings import *
from tile import Tile
from hero import Hero
# from piller1 import Piller
# from wall import Wall
from support import import_csv_layout, import_folder
from random import choice
from debug import *
from weapon import Weapon
from ui import UI
from enemy import Enemy


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.map_make()

        # user interface
        self.ui = UI()

    def map_make(self):
        layouts = {
            'boundary': import_csv_layout('../level_map/game_map1_border.csv'),
            'object': import_csv_layout('../level_map/game_map1_trees.csv'),
            'grass': import_csv_layout('../level_map/game_map1_grass.csv'),
            'entities': import_csv_layout('../level_map/game_map1_enemy.csv')
        }

        graphics = {
            'grass': import_folder('../level_map/grass'),
            'object': import_folder('../level_map/trees')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'grass':
                            # need to get grass in the game.
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)

                        if style == 'object':
                            surf = graphics['object'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'entities':
                            if col == '394':
                                self.player = Hero(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                if col == 0:
                                    monster_name = 'slime'
                                elif col == 1:
                                    monster_name = 'knight'
                                elif col == 392:
                                    monster_name = 'mino'
                                elif col == 3:
                                    monster_name = 'dual_knight'
                                else:
                                    monster_name = 'slime'
                                Enemy(monster_name, (x, y), [self.visible_sprites])
        #         if col == 'x':
        #            Tile(pos=(x, y), groups=[self.visible_sprites, self.obstacle_sprites])

        #         if col == 'p1':
        #            Piller(pos=(x, y), groups=[self.visible_sprites, self.obstacle_sprites])

        #         if col == 'w':
        #             Wall(pos=(x, y), groups=[self.visible_sprites, self.obstacle_sprites])

        #         if col == 'p':
        #             self.player = Hero((x, y), [self.visible_sprites], self.obstacle_sprites)

        # self.player = Hero((3970, 9950),
        #                     [self.visible_sprites],
        #                     self.obstacle_sprites,
        #                     self.create_attack,
        #                     self.destroy_attack,
        #                     self.create_magic)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])
        # hero = , groups =

    def create_magic(self, style, strenth, cost):
        print(style)
        print(strenth)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        # Update and draw the game.
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        # debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):
    """this spread group is going to function as a camera.
    it also sorts the sprites by there y coordinate in order ot give some overlap"""
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Creating the floor
        self.floor_surf = pygame.image.load('../level_map/level1map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, hero):

        # getting the offset
        self.offset.x = hero.rect.centerx - self.half_width
        self.offset.y = hero.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
