import pygame

# PIPE CLASS
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap):
        pygame.sprite.Sprite.__init__(self)

        self.pipe_gap = pipe_gap
        self.image = pygame.image.load( "assets/pipe.png" )
        self.rect = self.image.get_rect()

        # IF POSITION VAR == 1 THEN IT'S THE TOP PIPE, ELSE IT'S THE BOTTOM ONE
        if position == 1:
            self.image = pygame.transform.flip( self.image, False, True )
            self.rect.bottomleft    = [x, y - int(pipe_gap / 2) ]

        if position == -1:
            self.rect.topleft       = [x, y + int(pipe_gap / 2) ]

    # UPDATE THE PIPE X COORD LOCATION
    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        # MEMORY OVERFLOW FIX - KILL THE PIPE IF IT REACHES END OF THE SCREEN
        if self.rect.right < 0:
            self.kill()
