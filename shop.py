import pygame
from button import Button

class Shop():
    def __init__(self,x,y,image, width, height, health):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
        self.width = width
        self.height = height
        self.health = health
        self.button_clicked = False
        
    def draw(self, screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))
        
    def update_health(self, screen, score):
        healthImage=pygame.image.load('assets/health.png')
        buttonBuyHealth=Button(self.width//2-200, self.height//2-300, healthImage)
        healthPrice=9

        if buttonBuyHealth.draw(screen):
            if not self.button_clicked:
                if score >= healthPrice:
                    self.health += 1
                    score -= healthPrice
                    self.button_clicked = True
                    return self.health, score
        if not pygame.mouse.get_pressed()[0]:
            self.button_clicked = False
        return self.health, score