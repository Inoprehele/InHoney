import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Honeymoil - добыча мёда 🐝")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BEE_YELLOW = (255, 223, 0)
HONEY_COLOR = (255, 180, 60)
GREEN = (34, 177, 76)
BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

font = pygame.font.SysFont(None, 24)

# Глобальные переменные
money = 50
honey_price = 5

# Классы
class Flower:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(150, HEIGHT - 50)
        self.nectar = random.randint(5, 10)
        self.visible = False  # 🌸 Сначала цветок скрыт

    def draw(self):
        if self.visible:
            pygame.draw.circle(screen, GREEN, (self.x, self.y), 10)

class Hive:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.honey = 0
        self.bees = [Bee(self) for _ in range(3)]

    def update(self):
        for bee in self.bees:
            bee.update()

    def draw(self):
        pygame.draw.rect(screen, BROWN, (self.x - 15, self.y - 15, 30, 30))
        for bee in self.bees:
            bee.draw()
        # Показать количество мёда
        text = font.render(f"{int(self.honey)}🍯", True, BLACK)
        screen.blit(text, (self.x - 10, self.y - 30))

class Bee:
    def __init__(self, hive):
        self.hive = hive
        self.x = hive.x
        self.y = hive.y
        self.state = "to_flower"
        self.target = self.find_visible_flower()
        self.timer = 0
        self.carrying = 0

    def find_visible_flower(self):
        visible_flowers = [f for f in flowers if f.visible and f.nectar > 0]
        return random.choice(visible_flowers) if visible_flowers else None

    def update(self):
        if self.state == "to_flower":
            if not self.target or self.target.nectar <= 0:
                self.target = self.find_visible_flower()
                if not self.target:
                    return  # Нет цели
            self.move_towards(self.target.x, self.target.y)
            if self.close_to(self.target.x, self.target.y):
                self.state = "collecting"
                self.timer = 60
        elif self.state == "collecting":
            self.timer -= 1
            if self.timer <= 0:
                collected = min(1, self.target.nectar)
                self.target.nectar -= collected
                self.carrying = collected
                self.state = "returning"
        elif self.state == "returning":
            self.move_towards(self.hive.x, self.hive.y)
            if self.close_to(self.hive.x, self.hive.y):
                self.hive.honey += self.carrying
                self.carrying = 0
                self.state = "to_flower"
                self.target = self.find_visible_flower()

    def move_towards(self, tx, ty):
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)
        if dist > 1:
            self.x += dx / dist * 2
            self.y += dy / dist * 2

    def close_to(self, tx, ty):
        return abs(self.x - tx) < 5 and abs(self.y - ty) < 5

    def draw(self):
        pygame.draw.circle(screen, BEE_YELLOW, (int(self.x), int(self.y)), 5)

# Цветки и ульи
flowers = [Flower() for _ in range(20)]
hives = []

# Функция: открыть цветки в радиусе 100px
def reveal_flowers_near_hives():
    for flower in flowers:
        for hive in hives:
            dx = flower.x - hive.x
            dy = flower.y - hive.y
            distance = math.hypot(dx, dy)
            if distance <= 100:
                flower.visible = True
                break

# Игровой цикл
running = True
while running:
    screen.fill(BLUE)

    # Цветки
    for flower in flowers:
        flower.draw()

    # Ульи и пчёлы
    for hive in hives:
        hive.update()
        hive.draw()

    # Интерфейс
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 40))
    ui_text = font.render(f"Деньги: ${money} | [ЛКМ] улей ($30) | [ПКМ] продать | [C] скан", True, BLACK)
    screen.blit(ui_text, (10, 10))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y > 50:
                if event.button == 1 and money >= 30:
                    hives.append(Hive(x, y))
                    money -= 30
                elif event.button == 3:
                    for hive in hives:
                        if hive.honey >= 1:
                            sell = int(hive.honey)
                            money += sell * honey_price
                            hive.honey = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                reveal_flowers_near_hives()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
