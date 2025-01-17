import pygame
from button import Button

class SkinMenu:
    def __init__(self, screen, skins, costs):
        """
        Конструктор меню скинов.
        :param screen: экран для отрисовки
        :param skins: список скинов (каждый скин - список из кадров анимации)
        :param costs: стоимость каждого скина
        """
        self.screen = screen
        self.skins = skins  # Список скинов
        self.costs = costs  # Стоимость каждого скина
        self.purchased = [False] * len(skins)  # Статус покупки для каждого скина
        self.purchased[0] = True  # Первый скин всегда куплен
        self.selected_skin = 0  # Текущий выбранный скин
        self.font = pygame.font.SysFont('Bauhaus 93', 30)
        self.back_button_img = pygame.image.load('assets/back_button.png')  # Кнопка "Back"

        # Генерация кнопок для скинов
        self.skin_buttons = []
        for i in range(len(skins)):
            x = 100 + i * 200
            y = 200
            self.skin_buttons.append(Button(x, y, skins[i][0]))  # Используем первый кадр как иконку

    def draw(self, coins):
        """
        Отрисовка меню скинов.
        :param coins: количество монет у игрока
        :return: None, если ничего не выбрано, "back_to_gameover" для возврата
        """
        # Фон меню
        pygame.draw.rect(self.screen, (50, 50, 50), (50, 50, self.screen.get_width() - 100, self.screen.get_height() - 100))
        pygame.draw.rect(self.screen, (200, 200, 200), (50, 50, self.screen.get_width() - 100, self.screen.get_height() - 100), 5)

        # Заголовок
        title = self.font.render("SKINS MENU", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 60))

        # Отображение скинов
        for i, button in enumerate(self.skin_buttons):
            # Кнопка с иконкой
            if button.draw(self.screen):  # Если кнопка нажата
                if not self.purchased[i]:  # Если скин ещё не куплен
                    if coins >= self.costs[i]:  # Проверяем, хватает ли монет
                        self.purchased[i] = True
                        coins -= self.costs[i]
                if self.purchased[i]:  # Если скин уже куплен, то он становится выбранным
                    self.selected_skin = i

            # Текст: "Purchased" или цена
            x, y = button.rect.topleft
            if self.purchased[i]:
                text = self.font.render("Purchased", True, (0, 255, 0))
            else:
                text = self.font.render(f"{self.costs[i]} coins", True, (255, 255, 255))
            self.screen.blit(text, (x + 10, y - 30))  # Текст выше кнопки

            # Обводка выбранного скина
            if i == self.selected_skin:
                pygame.draw.rect(self.screen, (255, 255, 0), button.rect, 3)

        # Монеты игрока
        coins_text = self.font.render(f"Coins: {coins}", True, (255, 255, 0))
        self.screen.blit(coins_text, (100, self.screen.get_height() - 150))

        # Кнопка "Back"
        back_button = Button(50, self.screen.get_height() - 100, self.back_button_img)
        if back_button.draw(self.screen):
            return "back_to_gameover", coins

        return None, coins

    def handle_event(self, event):
        """
        Обработка событий меню скинов (больше не нужна логика покупки здесь).
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_skin = (self.selected_skin - 1) % len(self.skins)
            elif event.key == pygame.K_RIGHT:
                self.selected_skin = (self.selected_skin + 1) % len(self.skins)
            elif event.key == pygame.K_ESCAPE:
                return False  # Закрыть меню
        return True

    def get_selected_skin(self):
        """
        Возвращает текущий выбранный скин.
        """
        return self.selected_skin
