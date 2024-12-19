import pygame
from pygame.locals import *

pygame.init()

clock=pygame.time.Clock()
fps=60

width=864
height=936
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

ground_y=768
ground_scroll=0
scroll_speed=4
flying=False
game_over=False

background=pygame.image.load('assets/bg.png')
ground=pygame.image.load('assets/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for number in range(1,4):
            img = pygame.image.load(f'assets/bird{number}.png')
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.velocity=0
        self.clicked=False

    def update(self):
        if flying:
            self.velocity+=0.5
            if self.velocity>8:
                self.velocity=8
            if self.rect.bottom < ground_y:
                self.rect.y+=int(self.velocity)
        if game_over==False:
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                self.velocity=-10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False

            self.counter+=1
            cooldown=5
            if self.counter > cooldown:
                self.counter=0
                self.index+=1
                if self.index >= len(self.images):
                    self.index=0
            self.image=self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.velocity*-3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

bird_group = pygame.sprite.Group()
flappy=Bird(100, int(height/2))
bird_group.add(flappy)
        

run=True
while run:
    clock.tick(fps)

    screen.blit(background,(0,0))
    screen.blit(ground,(ground_scroll,ground_y))
    
    bird_group.draw(screen)
    bird_group.update()

    if flappy.rect.bottom > ground_y:
        game_over=True
        flying=False
    
    if game_over==False:
        ground_scroll-=scroll_speed
        if abs(ground_scroll)>35:
            ground_scroll=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True
    pygame.display.update()
pygame.quit()