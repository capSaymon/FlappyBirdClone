import pygame
import random # FOR PIPE RANDOM Y COORD POSITION MECHANISM
pygame.init()

# PARAMS
clock           = pygame.time.Clock()
fps             = 60
width           = 864
height          = 936
ground_y        = 768
ground_scroll   = 0
scroll_speed    = 4
pipe_gap        = 150                       # px
pipe_frequency  = 1500                      # ms
last_pipe       = pygame.time.get_ticks() - pipe_frequency # CREATE THE PIPE IMMEDIATELY AFTER STARTING THE GAME

flying          = False
game_over       = False

screen          = pygame.display.set_mode( (width, height) )
background      = pygame.image.load( 'assets/bg.png'       )
ground          = pygame.image.load( 'assets/ground.png'   )
pygame.display.set_caption('Flappy Bird')


# BIRD CLASS
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images         = []
        self.index          = 0
        self.counter        = 0
        for number in range(1, 4):
            img = pygame.image.load( f'assets/bird{number}.png' )
            self.images.append( img )
        self.image          = self.images[self.index]
        self.rect           = self.image.get_rect()
        self.rect.center    = [x, y]
        self.velocity       = 0
        self.clicked        = False

    def update(self):
        if flying:
            self.velocity += 0.5
            if self.velocity > 8:               self.velocity = 8
            if self.rect.bottom < ground_y:     self.rect.y += int(self.velocity)
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            cooldown = 5
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# PIPE CLASS
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load( "assets/pipe.png" )
        self.rect = self.image.get_rect()

        # IF POSITION VAR == 1 THEN IT'S THE TOP PIPE, ELSE IT'S THE BOTTOM ONE
        if position == 1:
            self.image = pygame.transform.flip( self.image, False, True )
            self.rect.bottomleft    = [x, y - int(pipe_gap / 2) ]

        if position == -1:
            self.rect.topleft       = [x, y + int(pipe_gap / 2) ]

    # UPDATE THE PIPE X COORD LOCATION
    def update(self):
        self.rect.x -= scroll_speed
        # MEMORY OVERFLOW FIX - KILL THE PIPE IF IT REACHES END OF THE SCREEN
        if self.rect.right < 0:
            self.kill()

# GROUPS
bird_group      = pygame.sprite.Group()
pipe_group      = pygame.sprite.Group()
flappy          = Bird(100, int(height / 2))
bird_group.add(flappy)


# GAME LOOP
run = True
while run:
    clock.tick(fps)

    screen.blit(background, (0, 0))
    screen.blit(ground, (ground_scroll, ground_y))

    bird_group.draw(screen)
    bird_group.update()

    # DRAW THE PIPE ON THE SCREEN
    pipe_group.draw(screen)

    # LOOK FOR COLLISION BETWEEN THE BIRD AND THE PIPE, BUT DON'T DELETE THE GROUPS
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= ground_y:
        game_over = True
        flying = False

    # CHECK IF THE GAME IS RUNNING AND THE BIRD IS FLYING
    if game_over == False and flying == True:

        # GENERATE NEW PIPES
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:

            pipe_height = random.randint(-100 , 100)
            btm_pipe    = Pipe(width, int(height / 2) + pipe_height, -1)
            top_pipe    = Pipe(width, int(height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # UPDATE THE PIPE LOCATION
        pipe_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                                           run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:     flying = True
    pygame.display.update()
pygame.quit()