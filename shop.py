import pygame

class Shop():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
