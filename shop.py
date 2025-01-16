import pygame
from button import Button

#GUI sklepu do fllapy bird
#posiada przyciski powrotu i kupna boosta
#boost 1: serca

class Shop():
    #konstruktor
    def __init__(self,x,y,image, width, height, health):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
        self.width = width
        self.height = height
        self.health = health
        self.button_clicked = False

        
    #funkcja tworząca GUI sklepu
    def draw(self, screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))


    #funkcja odpowiedzialna za napisy cen
    def text(self, screen, text, x, y, size):
        font=pygame.font.SysFont('Bauhus 93', size)
        color=(255,255,255)
        img=font.render(text,True, color)
        screen.blit(img,(x,y))      


    #funkcja odpowiedzialna za napis score
    def score_shop(self, screen, score):
        self.text(screen, f"Score: {score}", self.width // 2 - 350, 100, 50)


    #funkcja tworząca przycisk kupna boosta serc
    def update_health(self, screen, score, actualHealth, healthImage):

        #zmienne odpowiedzialne za rozmieszczenie przycisku oraz ceny pod nim
        x = 100
        y = self.height//2-250
        gap = 50

        #cena
        healthPrice=10

        #przycisk boosta oraz cena
        buttonBuyHealth=Button(x, y, healthImage)
        self.text(screen, f"Price: {healthPrice}", x, y + gap, 40)

        #sprawdzanie czy klawisz został przyciśniety
        if buttonBuyHealth.draw(screen):
            if not self.button_clicked:

                #ograniczona ilość kupna boosta
                if actualHealth < 5:

                    #sprawdzenie czy można kupić boosta, jeżeli tak to nadaje boosta oraz odejmuje cene
                    if score >= healthPrice:
                        self.health += 1
                        score -= healthPrice
                        self.button_clicked = True

                        #zwrot ilości serc oraz socore, aby wprowadzić zmiany w pliku main
                        return self.health, score
                    
        #przycisk nie naciśnięty
        if not pygame.mouse.get_pressed()[0]:
            self.button_clicked = False
        
        #zwrot ilości serc oraz socore, aby wprowadzić zmiany w pliku main
        return self.health, score   


    #stworzenie przycisku (jako napisu) powrotu do GUI gameover
    def back_button (self, screen, imageButtonBack):

        #wartości tekstu
        text="BACK"
        font=pygame.font.SysFont('Bauhus 93', 40)
        color=(255,255,255)

        #lokalizacja
        x = int(self.width/2)+250
        y = 100

        #stworzenie przycisku
        text_img = font.render(text, True, color)
        text_rect = text_img.get_rect()
        text_rect.topleft = (x, y)
        buttonBack = Button(x, y, text_img)

        #sprawdzanie czy przycisk został naciśniety
        if buttonBack.draw(screen):
            if not self.button_clicked:
                self.button_clicked = True
                return False
        if not pygame.mouse.get_pressed()[0]:
            self.button_clicked = False
        return True