import pygame
import random
from bird import Bird
from pipe import Pipe
from button import Button
from shop import Shop

pygame.init()

clock=pygame.time.Clock()
fps=60
width=864
height=936
font=pygame.font.SysFont('Bauhus 93', 60)
text_color=(255,255,255)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

ground_y = 768
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
shopAction = False
health = 0
gap = 150
frequency = 1500
last_pipe = pygame.time.get_ticks()-frequency
score = 50
pass_pipe = False

background=pygame.image.load('assets/bg.png')
ground=pygame.image.load('assets/ground.png')
restart=pygame.image.load('assets/restart.png')

shopButtonImage=pygame.image.load('assets/shop.png')
shopBackground=pygame.image.load('assets/shopBackground.png')

heart=pygame.image.load('assets/heart.png')

bird_group=pygame.sprite.Group()
flappy=Bird(100, int(height/2))
bird_group.add(flappy)

pipe_group=pygame.sprite.Group()       


def score_text(text, font, color, x, y):
    img=font.render(text,True, color)
    screen.blit(img,(x,y))


buttonRestart=Button(width//2-50, height//2-100, restart)
shopButtonRestart=Button(width//2-50, height//2-395, restart)
shopButton=Button(width//2-50, height//2, shopButtonImage)
shop=Shop(0, 0, shopBackground, width, height, health)

def reset_game():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(height/2)
    score=0
    return score




run=True
while run:
    clock.tick(fps)

    if shopAction:
        shop.draw(screen)
        health, score = shop.update_health(screen, score)
        score_text(str(score), font, text_color, int(width/2),30)

        if game_over==True:
            if shopButtonRestart.draw(screen)==True:
                game_over=False
                shopAction=False
                score=reset_game()

    else:
        screen.blit(background,(0,0))

        bird_group.draw(screen)
        bird_group.update(ground_y, game_over, flying)
        pipe_group.draw(screen)

        screen.blit(ground,(ground_scroll,ground_y))

        if len(pipe_group)>0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
                pass_pipe=True
            if pass_pipe==True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score+=1
                    pass_pipe=False

        score_text(str(score), font, text_color, int(width/2),30)

        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top<0:
            game_over=True

        if flappy.rect.bottom >= ground_y:
            game_over=True
            flying=False

        if game_over==False and flying==True:
            time_now=pygame.time.get_ticks()
            if time_now-last_pipe>frequency:
                pipe_height=random.randint(-100,100)
                top_pipe=Pipe(width,int(height/2)+pipe_height,1,gap)
                btm_pipe=Pipe(width,int(height/2)+pipe_height,-1,gap)
                pipe_group.add(top_pipe)
                pipe_group.add(btm_pipe)
                last_pipe=time_now

            ground_scroll-=scroll_speed
            if abs(ground_scroll)>35:
                ground_scroll=0
                
            pipe_group.update(scroll_speed)

        if health > 0:
            x  = 20
            y = 20
            for i in range(health):
                screen.blit(heart, (x, y))
                x += 40
        
    #check for game over, reset and shop
    if game_over==True:
        if shopAction==False:
            if buttonRestart.draw(screen)==True:
                game_over=False
                score=reset_game()
            if shopButton.draw(screen)==True:
                shopAction=True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True
    pygame.display.update()
pygame.quit()