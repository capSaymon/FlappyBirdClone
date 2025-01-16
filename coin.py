# ========================== Copyright © 2024-2025, Flappy Bird Clone, All rights reserved. ========================== #
#                                                                                                                      #
#                                   Purpose: Coin class, describes the coin object.                                    #
#                                                                                                                      #
# ==================================================================================================================== #

import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/coin.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()