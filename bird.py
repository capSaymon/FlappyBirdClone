import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, animation_frames):
        """
        Конструктор класса Bird.
        :param x: начальная координата x
        :param y: начальная координата y
        :param animation_frames: список кадров анимации для птицы
        """
        super().__init__()
        self.animation_frames = animation_frames  # Список кадров для анимации
        self.index = 0  # Индекс текущего кадра
        self.counter = 0  # Счётчик для смены кадров
        self.image = self.animation_frames[self.index]  # Устанавливаем начальный кадр
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = 0  # Скорость перемещения
        self.clicked = False  # Флаг для предотвращения постоянного прыжка

    def set_skin(self, animation_frames):
        """
        Метод для смены скина птицы.
        :param animation_frames: список новых кадров для анимации
        """
        self.animation_frames = animation_frames
        self.index = 0  # Сбрасываем индекс анимации
        self.image = self.animation_frames[self.index]  # Устанавливаем новый кадр

    def update(self, ground_y, game_over, flying):
        """
        Обновление состояния птицы: гравитация, анимация, ротация.
        :param ground_y: координата y земли
        :param game_over: флаг окончания игры
        :param flying: флаг, указывающий, находится ли птица в полёте
        """
        if flying:
            # Применение гравитации
            self.velocity += 0.5
            if self.velocity > 8:  # Максимальная скорость падения
                self.velocity = 8
            if self.rect.bottom < ground_y:
                self.rect.y += int(self.velocity)

        if not game_over:
            # Реализация прыжка
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Смена кадров для анимации
            self.counter += 1
            if self.counter > 5:  # Задержка между кадрами
                self.counter = 0
                self.index = (self.index + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.index]

            # Ротация птицы при полёте
            self.image = pygame.transform.rotate(self.animation_frames[self.index], self.velocity * -3)
        else:
            # Ротация при завершении игры
            self.image = pygame.transform.rotate(self.animation_frames[self.index], -90)
