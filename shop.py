import pygame
from button import Button

class Shop:
    def __init__(self, x, y, image, width, height, health):
        """
        Конструктор класса Shop.
        :param x: координата x для фона магазина
        :param y: координата y для фона магазина
        :param image: фон магазина
        :param width: ширина экрана
        :param height: высота экрана
        :param health: текущее количество здоровья игрока
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = width
        self.height = height
        self.health = health
        self.button_clicked = False

    def draw(self, screen):
        """
        Отрисовка магазина.
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Загрузка кнопки здоровья
        health_button = Button(100, 100, pygame.image.load('assets/health.png'))  # Позиция кнопки Health
        self.text(screen, "Price: 10", 100, 180, 30)  # Позиция текста цены

        # Обработка клика по кнопке здоровья
        if health_button.draw(screen):
            if not self.button_clicked:
                self.button_clicked = True
                return "buy_health"

        # Кнопка "Back"
        back_button_img = pygame.image.load('assets/back_button.png')
        back_button = Button(50, self.height - 100, back_button_img)
        if back_button.draw(screen):
            return "back_to_gameover"

        # Сброс клика мыши
        if not pygame.mouse.get_pressed()[0]:
            self.button_clicked = False

        return None

    def text(self, screen, text, x, y, size):
        """
        Рисует текст на экране.
        :param screen: экран, на котором рисуется текст
        :param text: текст для отображения
        :param x: координата x
        :param y: координата y
        :param size: размер шрифта
        """
        font = pygame.font.SysFont('Bauhaus 93', size)
        color = (255, 255, 255)
        img = font.render(text, True, color)
        screen.blit(img, (x, y))
