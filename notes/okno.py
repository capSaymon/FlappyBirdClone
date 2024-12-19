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

background=pygame.image.load('assets/bg.png')
ground=pygame.image.load('assets/ground.png')

run=True
while run:
    clock.tick(fps)

    screen.blit(background,(0,0))
    screen.blit(ground,(ground_scroll,ground_y))
    ground_scroll-=scroll_speed
    if abs(ground_scroll)>35:
        ground_scroll=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()