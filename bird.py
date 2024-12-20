import pygame

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

    def update(self, ground_y, game_over, flying):
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

