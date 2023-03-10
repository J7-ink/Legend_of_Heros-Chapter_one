import pygame
from settings import *


class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # health/energy bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictionary to list.
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # convert skill dictionary to list.
        self.skill_graphics = []
        for skill in skill_data.values():
            path = skill['graphic']
            skill = pygame.image.load(path).convert_alpha()
            self.skill_graphics.append(skill)

    def show_bar(self, current, max_amount, background_rect, color):
        # draw the background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, background_rect)

        # converting stats to pixels
        ratio = current / max_amount
        current_width = background_rect.width * ratio
        current_rect = background_rect.copy()
        current_rect.width = current_width

        # draw the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, current_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        # render needs info,AA, color. AA = antialiasing
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 15
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(15, 15))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(15, 15), 3)

    def selection_box(self, left, top, has_switched):
        background_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, background_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, background_rect, 3)
            #
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, background_rect, 3)
        return background_rect

    def weapon_overlay(self, weapon_index, has_switched):
        background_rect = self.selection_box(10, 544, has_switched)  # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=background_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def skill_overlay(self, magic_index, has_switched):
        background_rect = self.selection_box(10, 630, has_switched)  # skill/magic
        skill_surf = self.skill_graphics[magic_index]
        skill_rect = skill_surf.get_rect(center=background_rect.center)

        self.display_surface.blit(skill_surf, skill_rect)

    def display(self, player):

        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.skill_overlay(player.magic_index, not player.can_switch_magic)
        # self.selection_box(10, 544) # skills

        # self.selection_box(95, 630)

        # pygame.draw.rect(self.display_surface, 'black', self.health_bar_rect)
