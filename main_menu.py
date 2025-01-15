import pygame
import sys



class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()


        try:
            self.background_image = pygame.image.load('assets/bg.png')
            self.ground_image = pygame.image.load('assets/ground.png')
            self.title_image = pygame.image.load('assets/label_flappy_bird.png')
            self.get_ready_image = pygame.image.load('assets/label_get_ready.png')
            self.instructions_image = pygame.image.load('assets/instructions.png')
        except pygame.error as e:
            print(f"Помилка завантаження зображення: {e}")
            sys.exit()

        # Масштабування для відповідності екрану
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height - 100))
        self.ground_image = pygame.transform.scale(self.ground_image, (self.width, 100))
        self.title_image = pygame.transform.scale(self.title_image, (500, 150))  # Збільшено
        self.get_ready_image = pygame.transform.scale(self.get_ready_image, (400, 120))  # Збільшено
        self.instructions_image = pygame.transform.scale(self.instructions_image, (300, 300))  # Збільшено
    def draw(self):
        # Відображення фону
        self.screen.blit(self.background_image, (0, 0))

        # Відображення тексту та зображень
        self.screen.blit(self.title_image, (self.width // 2 - self.title_image.get_width() // 2, 50))
        self.screen.blit(self.get_ready_image,
                         (self.width // 2 - self.get_ready_image.get_width() // 2, 250))  # Опущено
        self.screen.blit(self.instructions_image,
                         (self.width // 2 - self.instructions_image.get_width() // 2, 450))  # Збільшено

        # Відображення землі
        self.screen.blit(self.ground_image, (0, self.height - self.ground_image.get_height()))


# Ігровий цикл
def main():
    # Ініціалізація Pygame
    pygame.init()
    screen = pygame.display.set_mode((864, 936))
    pygame.display.set_caption("Flappy Bird Menu")
    clock = pygame.time.Clock()
    fps = 60

    # Створення головного меню
    menu = MainMenu(screen)

    # Логіка ігрового процесу
    run = True
    game_started = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                game_started = True  # Логіка початку гри
                print("Гра почалася!")  # Поки що просто повідомлення в консоль

        # Малювання меню або ігрового процесу
        if not game_started:
            menu.draw()
        else:
            # Код для основної гри буде тут
            screen.fill((0, 0, 0))  # Просто чорний екран для ігрового процесу

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
