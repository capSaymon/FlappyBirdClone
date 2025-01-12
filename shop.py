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

    def price_text(self, screen, text, x, y):
        font=pygame.font.SysFont('Bauhus 93', 40)
        color=(255,255,255)
        img=font.render(text,True, color)
        screen.blit(img,(x,y))
        
    def update_health(self, screen, score, actualHealth, healthImage):
        x = self.width//2-200
        y = self.height//2-300
        healthPrice=10

        buttonBuyHealth=Button(x, y, healthImage)
        self.price_text(screen, f"Price: {healthPrice}", x, y + 50)

        if buttonBuyHealth.draw(screen):
            if not self.button_clicked:
                if actualHealth < 5:
                    if score >= healthPrice:
                        self.health += 1
                        score -= healthPrice
                        self.button_clicked = True
                        return self.health, score
        if not pygame.mouse.get_pressed()[0]:
            self.button_clicked = False
        return self.health, score
    
    def back_button (self, screen, imageButtonBack):
        buttonBack=Button(self.width//2-60, self.height//2-380, imageButtonBack)
        if buttonBack.draw(screen):
            if not self.button_clicked:
                self.button_clicked = True
                return False
        if not pygame.mouse.get_pressed()[0]:
            self.button_clicked = False
        return True