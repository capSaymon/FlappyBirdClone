# ========================== Copyright © 2024-2025, Flappy Bird Clone, All rights reserved. ========================== #
#                                                                                                                      #
#                                   Purpose: Main file, executes the entire game.                                      #
#                                     Stores all the code except game classes.                                         #
#                                                                                                                      #
# ==================================================================================================================== #

import pygame
import random       # BIBLIOTEKA POTRZEBNA DO GENEROWANIA PRZESTRZENI MIĘDZY RURAMI W LOSOWYM MIEJSCU ZMIENNEJ Y

# Project custom class imports
from bird       import Bird
from pipe       import Pipe
from coin       import Coin
from shop       import Shop
from button     import Button
from main_menu  import MainMenu

pygame.init()
clock   = pygame.time.Clock()

# -------------------------------------------------------------------------------------------------------------------- #
#                                                Game settings                                                         #
# -------------------------------------------------------------------------------------------------------------------- #

GAME_FPS            = 60
GAME_WIDTH          = 864
GAME_HEIGHT         = 936
GAME_TITLE          = 'Flappy Bird'
GAME_FONT           = pygame.font.SysFont('Bauhaus 93', 60)
GAME_FONT_COLOR     = (255, 255, 255)
GAME_SCREEN         = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

pygame.display.set_caption(GAME_TITLE)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               Global Variables                                                       #
# -------------------------------------------------------------------------------------------------------------------- #

ground_y            = 768
ground_scroll       = 0
scroll_speed        = 4
health              = 0
healthSave          = 0
gap                 = 150                                 # PIXELE
frequency           = 1500                                # MILISEKUNDY
score               = 0
pass_pipe           = False
flying              = False
game_over           = False
shopAction          = False
paused              = False
healthAction        = False
last_pipe           = pygame.time.get_ticks() - frequency # UTWÓRZ PIERWSZE RURY NATYCHMIASTOWO PO URUCHOMIENIU GRY

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   Assets                                                             #
# -------------------------------------------------------------------------------------------------------------------- #

background          = pygame.image.load('assets/bg.png')
ground              = pygame.image.load('assets/ground.png')
restart_img         = pygame.image.load('assets/restart.png')
menuGameOver        = pygame.image.load('assets/menuGameOver.png')
shop_button_img     = pygame.image.load('assets/shop.png')
shop_background     = pygame.image.load('assets/shopBackground.png')
health_img          = pygame.image.load('assets/health.png')
heart               = pygame.image.load('assets/heart.png')
pause_button_img    = pygame.transform.scale(pygame.image.load('assets/button_pause.png'), (100, 100))
resume_button_img   = pygame.transform.scale(pygame.image.load('assets/button_resume.png'), (100, 100))

# -------------------------------------------------------------------------------------------------------------------- #
#                                               Groups & Buttons                                                       #
# -------------------------------------------------------------------------------------------------------------------- #

bird_group          = pygame.sprite.Group()
pipe_group          = pygame.sprite.Group()
coin_group          = pygame.sprite.Group()

flappy              = Bird(100, GAME_HEIGHT // 2)
bird_group.add(flappy)

button_restart      = Button(GAME_WIDTH // 2 - 50, GAME_HEIGHT // 2 - 20, restart_img)
shop_button         = Button(GAME_WIDTH // 2 - 50, GAME_HEIGHT // 2 + 40, shop_button_img)
pause_button        = Button(GAME_WIDTH - 120, 10, pause_button_img)
resume_button       = Button(GAME_WIDTH - 120, 10, resume_button_img)
shop                = Shop(0, 0, shop_background, GAME_WIDTH, GAME_HEIGHT, health)

def score_text(text, font, color, x, y):
    img = font.render(text, True, color)
    GAME_SCREEN.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = GAME_HEIGHT // 2
    return score

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   Game loop                                                          #
# -------------------------------------------------------------------------------------------------------------------- #

run                 = True
game_started        = False
menu                = MainMenu(GAME_SCREEN)

while run:
    clock.tick(GAME_FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not paused:
                if pause_button.rect.collidepoint(pygame.mouse.get_pos()):
                    paused = True
            else:
                if resume_button.rect.collidepoint(pygame.mouse.get_pos()):
                    paused = False

    if not game_started:
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_started = True
                flying = True
                flappy.velocity = -10
    else:
        if paused:
            GAME_SCREEN.blit(background, (0, 0))
            bird_group.draw(GAME_SCREEN)
            pipe_group.draw(GAME_SCREEN) # METODA ODPOWIEDZIALNA ZA RYSOWANIE RUR NA EKRANIE
            GAME_SCREEN.blit(ground, (ground_scroll, ground_y))
            resume_button.draw(GAME_SCREEN)
            score_text(f"Paused", GAME_FONT, GAME_FONT_COLOR, GAME_WIDTH // 2 - 100, GAME_HEIGHT // 2 - 50)
        else:
            if shopAction:
                #stworzenie GUI sklepu
                shop.draw(GAME_SCREEN)

                #stworzenie w GUI sklepu tekstu wyświetlania score
                shop.score_shop(GAME_SCREEN, score)

                #stworzenie przycisku boosta "serc"
                health, score = shop.update_health(GAME_SCREEN, score, healthSave, health_img)
                #zapisanie na stałe ilości serc
                healthSave = health

                #stworzenie przycisku BACK
                shopAction = shop.back_button(GAME_SCREEN, restart_img)
            else:
                GAME_SCREEN.blit(background, (0, 0))

                bird_group.draw(GAME_SCREEN)
                bird_group.update(ground_y, game_over, flying)
                pipe_group.draw(GAME_SCREEN)

                GAME_SCREEN.blit(ground, (ground_scroll, ground_y))

                if len(pipe_group) > 0:
                    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and \
                       bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and not pass_pipe:
                        pass_pipe = True
                    if pass_pipe:
                        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                            score += 1
                            healthAction = False
                            pass_pipe = False

                if not game_over:
                    score_text(str(score), GAME_FONT, GAME_FONT_COLOR, GAME_WIDTH // 2 - 10, 30)

                # SPRAWDZAJ CZY ZAISTNIAŁA KOLIZJA MIĘDZY PTAKIEM I RURĄ
                if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
                    if not healthAction:
                        health -= 1
                        healthAction = True
                        if health <= 0:
                            game_over = True
                if flappy.rect.top < 0:
                    game_over = True

                if flappy.rect.bottom >= ground_y:
                    game_over = True
                    flying = False

                if not game_over and flying:
                    # LOSOWA GENERACJA RUR
                    time_now = pygame.time.get_ticks()
                    if time_now - last_pipe > frequency:
                        pipe_height = random.randint(-100, 100)

                        top_pipe    = Pipe(GAME_WIDTH, GAME_HEIGHT // 2 + pipe_height, 1, gap)
                        bottom_pipe = Pipe(GAME_WIDTH, GAME_HEIGHT // 2 + pipe_height, -1, gap)

                        pipe_group.add(top_pipe)
                        pipe_group.add(bottom_pipe)

                        # LOSOWA GENERACJA MONET
                        if random.randint(1, 10) > 7:  # SZANSA: 30%
                            coin_y      = GAME_HEIGHT // 2 + pipe_height
                            new_coin    = Coin(GAME_WIDTH + 20, coin_y)
                            coin_group.add(new_coin)

                        last_pipe = time_now

                    ground_scroll -= scroll_speed
                    if abs(ground_scroll) > 35:
                        ground_scroll = 0

                    # AKTUALIZACJA GRUP
                    pipe_group.update(scroll_speed)
                    coin_group.update(scroll_speed)
                    coin_group.draw(GAME_SCREEN)

                    # DETEKCJA KOLIZJI Z MONETĄ (+1 DO SCORE)
                    coin_collision = pygame.sprite.spritecollide(flappy, coin_group, True)
                    if coin_collision:  score += 1

                if health > 0:
                    x = 20
                    y = 20
                    for i in range(health):
                        GAME_SCREEN.blit(heart, (x, y))
                        x += 40

            if game_over:
                if not shopAction:
                    GAME_SCREEN.blit(menuGameOver, (GAME_WIDTH // 2 - menuGameOver.get_width() // 2 + 10, GAME_HEIGHT // 2 - menuGameOver.get_height() // 2))
                    score_text(str(score), GAME_FONT, GAME_FONT_COLOR, GAME_WIDTH // 2 - 10, 370)
                    if button_restart.draw(GAME_SCREEN):
                        game_over = False
                        health = healthSave
                        score = reset_game()
                    if shop_button.draw(GAME_SCREEN):
                        shopAction = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                    flying = True

        if paused:
            resume_button.draw(GAME_SCREEN)
        else:
            if not game_over and flying:
                pause_button.draw(GAME_SCREEN)

    pygame.display.update()

pygame.quit()