import pygame
from pygame.locals import *
import random

pygame.init()

clock=pygame.time.Clock()
fps=60
width=864
height=936
font=pygame.font.SysFont('Bauhus 93', 60)
text_color=(255,255,255)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

ground_y=768
ground_scroll=0
scroll_speed=4
flying=False
game_over=False
gap=150
frequency=1500
last_pipe=pygame.time.get_ticks()-frequency
score=0
pass_pipe=False

background=pygame.image.load('assets/bg.png')
ground=pygame.image.load('assets/ground.png')
restart=pygame.image.load('assets/restart.png')


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
        self.vel=0
        self.clicked=False

    def update(self):
        if flying==True:
            self.vel+=0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < ground_y:
                self.rect.y+=int(self.vel)
        if game_over==False:
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                self.vel=-10
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

            self.image=pygame.transform.rotate(self.images[self.index], self.vel*-1)
        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90)

bird_group=pygame.sprite.Group()
flappy=Bird(100, int(height/2))
bird_group.add(flappy)


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('assets/pipe.png')
        self.rect=self.image.get_rect()
        if position == 1:
            self.image=pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft=[x,y-int(gap/2)]
        if position == -1:
            self.rect.topleft=[x,y+int(gap/2)]

    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()

pipe_group=pygame.sprite.Group()       


def score_text(text, font, color, x, y):
    img=font.render(text,True, color)
    screen.blit(img,(x,y))

class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True
        screen.blit(self.image,(self.rect.x, self.rect.y))
        return action

button=Button(width//2-50, height//2-100, restart)

def reset_game():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(height/2)
    score=0
    return score

run=True
while run:
    clock.tick(fps)
    screen.blit(background,(0,0))    

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground,(ground_scroll,ground_y))

    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe=True
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe=False

    score_text(str(score), font, text_color, int(width/2),20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top<0:
        game_over=True

    if flappy.rect.bottom >= ground_y:
        game_over=True
        flying=False

    if game_over==False and flying==True:
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>frequency:
            pipe_height=random.randint(-100,100)
            top_pipe=Pipe(width,int(height/2)+pipe_height,1)
            btm_pipe=Pipe(width,int(height/2)+pipe_height,-1)
            pipe_group.add(top_pipe)
            pipe_group.add(btm_pipe)
            last_pipe=time_now

        ground_scroll-=scroll_speed
        if abs(ground_scroll)>35:
            ground_scroll=0
            
        pipe_group.update()
        
    #check for game over and reset
    if game_over==True:
        if button.draw()==True:
            game_over=False
            score=reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True
    pygame.display.update()
pygame.quit()