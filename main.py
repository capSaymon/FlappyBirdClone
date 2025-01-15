import pygame
import random
from bird import Bird
from pipe import Pipe
from button import Button
from shop import Shop

from main_menu import MainMenu

pygame.init()

# Налаштування екрану
clock = pygame.time.Clock()
fps = 60
width, height = 864, 936
font = pygame.font.SysFont('Bauhaus 93', 60)
text_color = (255, 255, 255)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

# Змінні стану гри
ground_y = 768
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
shopAction = False
paused = False
health = 0
healthAction = False
healthSave = 0
gap = 150
frequency = 1500
last_pipe = pygame.time.get_ticks() - frequency
score = 50
pass_pipe = False

# Завантаження зображень
background = pygame.image.load('assets/bg.png')
ground = pygame.image.load('assets/ground.png')
restart_img = pygame.image.load('assets/restart.png')
menuGameOver = pygame.image.load('assets/menuGameOver.png')
shop_button_img = pygame.image.load('assets/shop.png')
shop_background = pygame.image.load('assets/shopBackground.png')
health_img = pygame.image.load('assets/health.png')
heart = pygame.image.load('assets/heart.png')
pause_button_img = pygame.transform.scale(pygame.image.load('assets/button_pause.png'), (100, 100))
resume_button_img = pygame.transform.scale(pygame.image.load('assets/button_resume.png'), (100, 100))

# Групи спрайтів
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# Ігрові об'єкти
flappy = Bird(100, height // 2)
bird_group.add(flappy)

button_restart = Button(width // 2 - 50, height // 2 - 20, restart_img)
shop_button = Button(width // 2 - 50, height // 2 + 40, shop_button_img)
pause_button = Button(width - 120, 10, pause_button_img)
resume_button = Button(width - 120, 10, resume_button_img)
shop = Shop(0, 0, shop_background, width, height, health)

# Текст для відображення очок
def score_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Скидання гри
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = height // 2
    return 0

# Основний цикл гри
run = True
game_started = False
menu = MainMenu(screen)

while run:
    clock.tick(fps)

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
            # Відображення паузи, але без оновлення об'єктів
            screen.blit(background, (0, 0))
            bird_group.draw(screen)
            pipe_group.draw(screen)
            screen.blit(ground, (ground_scroll, ground_y))
            resume_button.draw(screen)
            score_text(f"Paused", font, text_color, width // 2 - 100, height // 2 - 50)
        else:
            if shopAction:
                shop.draw(screen)
                fontShop = pygame.font.SysFont('Bauhaus 93', 50)
                score_text(f"Score: {score}", fontShop, text_color, width // 2 - 350, 100)
                health, score = shop.update_health(screen, score, healthSave, health_img)
                healthSave = health
                shopAction = shop.back_button(screen, restart_img)
            else:
                screen.blit(background, (0, 0))

                bird_group.draw(screen)
                bird_group.update(ground_y, game_over, flying)
                pipe_group.draw(screen)

                screen.blit(ground, (ground_scroll, ground_y))

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
                    score_text(str(score), font, text_color, width // 2 - 10, 30)

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
                    time_now = pygame.time.get_ticks()
                    if time_now - last_pipe > frequency:
                        # Визначення висоти колони
                        pipe_height = random.randint(-100, 100)

                        # Створення верхньої та нижньої колони
                        top_pipe = Pipe(width, height // 2 + pipe_height, 1, gap)
                        bottom_pipe = Pipe(width, height // 2 + pipe_height, -1, gap)

                        # Додавання пари колон до групи
                        pipe_group.add(top_pipe)
                        pipe_group.add(bottom_pipe)

                        # Оновлення часу останньої колони
                        last_pipe = time_now

                    ground_scroll -= scroll_speed
                    if abs(ground_scroll) > 35:
                        ground_scroll = 0

                    pipe_group.update(scroll_speed)

                if health > 0:
                    x = 20
                    y = 20
                    for i in range(health):
                        screen.blit(heart, (x, y))
                        x += 40

            if game_over:
                if not shopAction:
                    screen.blit(menuGameOver, (width // 2 - menuGameOver.get_width() // 2 + 10,
                                               height // 2 - menuGameOver.get_height() // 2))
                    score_text(str(score), font, text_color, width // 2 - 10, 370)
                    if button_restart.draw(screen):
                        game_over = False
                        health = healthSave
                        score = reset_game()
                    if shop_button.draw(screen):
                        shopAction = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                    flying = True

        if paused:
            resume_button.draw(screen)
        else:
            pause_button.draw(screen)

    pygame.display.update()

pygame.quit()
