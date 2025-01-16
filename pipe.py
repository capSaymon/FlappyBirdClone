# ========================== Copyright © 2024-2025, Flappy Bird Clone, All rights reserved. ========================== #
#                                                                                                                      #
#                                   Purpose: Pipe class, describes the pipe object.                                    #
#                                                                                                                      #
# ==================================================================================================================== #

import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap):
        pygame.sprite.Sprite.__init__(self)

        self.pipe_gap = pipe_gap
        self.image = pygame.image.load( "assets/pipe.png" )
        self.rect = self.image.get_rect()

        # WARTOŚĆ ZMIENNEJ POSITION DEFINIUJE POZYCJE RURY NA OSI Y (GÓRNA / DOLNA)
        if position == 1:
            self.image = pygame.transform.flip( self.image, False, True )
            self.rect.bottomleft    = [x, y - int(pipe_gap / 2) ]

        if position == -1:
            self.rect.topleft       = [x, y + int(pipe_gap / 2) ]

    # AKTUALIZACJA POZYCJI OBIEKTU NA OSI X
    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        # MEMORY OVERFLOW FIX - ZABIJ OBIEKT KIEDY DOTRZE DO KOŃCA EKRANU
        if self.rect.right < 0: self.kill()