import pygame
import sys
import random
from config import Settings, COLORS, SIZE_BLOCK, COUNT_BLOCK, HEADER_MARGIN, MARGIN, size
from db import Database

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y
    
    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCK and 0 <= self.y < COUNT_BLOCK

class Bonus:
    def __init__(self, x, y, bonus_type):
        self.x = x
        self.y = y
        self.type = bonus_type  # 'speed', 'slow', 'shield'
        self.spawn_time = pygame.time.get_ticks()
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 8000  # 8 секунд
    
    def __eq__(self, other):
        return isinstance(other, Bonus) and self.x == other.x and self.y == other.y

class Game:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings
        self.db = Database()
        
        # Параметры игры
        self.snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
        self.d_row = 0
        self.d_col = 1
        self.total = 0
        self.level = 1
        self.speed = 1
        self.walls = []
        self.active_bonus = None
        self.bonus_effect_end = 0
        self.bonus_effect_active = None
        self.shield_active = False
        
        # Создание еды, яда и бонусов
        self.food = None
        self.poison = None
        self.bonus = None
        
        # Теперь создаем объекты в правильном порядке
        self.food = self.get_random_empty_block()
        self.poison = self.get_random_empty_block()
        
        # Создаем часы для FPS
        self.clock = pygame.time.Clock()
        
        # Личный рекорд
        self.personal_best = self.db.get_player_best_score(username)
    
    def get_random_empty_block(self, exclude_walls=True):
        """Получение случайной пустой клетки"""
        x = random.randint(0, COUNT_BLOCK - 1)
        y = random.randint(0, COUNT_BLOCK - 1)
        empty_block = SnakeBlock(x, y)
        
        # Проверяем, не занята ли клетка
        while True:
            collision = False
            
            # Проверка столкновения со змеей
            if empty_block in self.snake_blocks:
                collision = True
            
            # Проверка столкновения с едой
            if self.food and empty_block == self.food:
                collision = True
            
            # Проверка столкновения с ядом
            if self.poison and empty_block == self.poison:
                collision = True
            
            # Проверка столкновения со стенами
            if exclude_walls and empty_block in self.walls:
                collision = True
            
            # Проверка столкновения с бонусом
            if self.bonus and empty_block == self.bonus:
                collision = True
            
            if not collision:
                break
            
            # Генерируем новую позицию
            empty_block.x = random.randint(0, COUNT_BLOCK - 1)
            empty_block.y = random.randint(0, COUNT_BLOCK - 1)
        
        return empty_block
    
    def generate_walls(self):
        """Генерация препятствий начиная с 3 уровня"""
        if self.level < 3:
            self.walls = []
            return
        
        wall_count = min(self.level * 2, 30)
        self.walls = []
        
        for _ in range(wall_count):
            wall = self.get_random_empty_block(exclude_walls=False)
            # Проверяем, не блокирует ли стена змею
            attempts = 0
            while (wall in self.snake_blocks or 
                   (self.food and wall == self.food) or 
                   (self.poison and wall == self.poison) or
                   (self.bonus and wall == self.bonus) or
                   wall in self.walls):
                wall = self.get_random_empty_block(exclude_walls=False)
                attempts += 1
                if attempts > 100:  # Предотвращаем бесконечный цикл
                    break
            self.walls.append(wall)
    
    def generate_bonus(self):
        """Генерация бонуса случайного типа"""
        if self.bonus is None and random.random() < 0.02:  # 2% шанс появления бонуса
            bonus_type = random.choice(['speed', 'slow', 'shield'])
            bonus_pos = self.get_random_empty_block()
            self.bonus = Bonus(bonus_pos.x, bonus_pos.y, bonus_type)
    
    def apply_bonus_effect(self, bonus_type):
        """Применение эффекта бонуса"""
        current_time = pygame.time.get_ticks()
        
        if bonus_type == 'speed':
            self.bonus_effect_active = 'speed'
            self.bonus_effect_end = current_time + 5000
        elif bonus_type == 'slow':
            self.bonus_effect_active = 'slow'
            self.bonus_effect_end = current_time + 5000
        elif bonus_type == 'shield':
            self.shield_active = True
            self.bonus_effect_active = 'shield'
            self.bonus_effect_end = current_time + 5000
    
    def update_speed(self):
        """Обновление скорости с учетом бонусов"""
        base_speed = 3 + self.speed
        
        if self.bonus_effect_active == 'speed':
            return base_speed + 3
        elif self.bonus_effect_active == 'slow':
            return max(1, base_speed - 2)
        return base_speed
    
    def check_bonus_expiry(self):
        """Проверка истечения эффекта бонуса"""
        current_time = pygame.time.get_ticks()
        
        if self.bonus_effect_active and current_time > self.bonus_effect_end:
            if self.bonus_effect_active == 'shield':
                self.shield_active = False
            self.bonus_effect_active = None
    
    def move_snake(self):
        head = self.snake_blocks[-1]
        new_head = SnakeBlock(head.x + self.d_row, head.y + self.d_col)
        
        # Проверка столкновений
        if not new_head.is_inside():
            if not self.shield_active:
                return False
            else:
                # С щитом: не умираем, но щит исчезает
                self.shield_active = False
                # Корректируем позицию
                new_head.x = max(0, min(COUNT_BLOCK - 1, new_head.x))
                new_head.y = max(0, min(COUNT_BLOCK - 1, new_head.y))
        
        if new_head in self.snake_blocks[1:] or new_head in self.walls:
            if not self.shield_active:
                return False
            else:
                self.shield_active = False
        
        self.snake_blocks.append(new_head)
        
        # Проверка поедания еды
        if new_head == self.food:
            self.total += 10
            self.speed = self.total // 50 + 1
            
            # Обновление уровня
            new_level = self.total // 50 + 1
            if new_level > self.level:
                self.level = new_level
                self.generate_walls()
            
            self.food = self.get_random_empty_block()
            self.poison = self.get_random_empty_block()
            self.generate_bonus()
            return True
        
        # Проверка поедания яда
        elif self.poison and new_head == self.poison:
            # Укорачиваем змею на 2 сегмента
            for _ in range(min(2, len(self.snake_blocks) - 1)):
                if len(self.snake_blocks) > 1:
                    self.snake_blocks.pop(0)
            
            if len(self.snake_blocks) <= 1:
                return False  # Game over
            
            self.poison = self.get_random_empty_block()
            return True
        
        # Проверка поедания бонуса
        elif self.bonus and new_head == self.bonus:
            self.apply_bonus_effect(self.bonus.type)
            self.bonus = None
            self.snake_blocks.pop(0)
            return True
        
        else:
            self.snake_blocks.pop(0)
            return True
    
    def draw(self, screen, font):
        # Отрисовка фона
        screen.fill(COLORS['FRAME'])
        pygame.draw.rect(screen, COLORS['HEADER'], [0, 0, size[0], HEADER_MARGIN])
        
        # Отрисовка сетки
        if self.settings.show_grid:
            for row in range(COUNT_BLOCK):
                for column in range(COUNT_BLOCK):
                    if (row + column) % 2 == 0:
                        color = COLORS['BLUE']
                    else:
                        color = COLORS['DBLUE']
                    self.draw_block(screen, color, row, column)
        else:
            for row in range(COUNT_BLOCK):
                for column in range(COUNT_BLOCK):
                    self.draw_block(screen, COLORS['DBLUE'], row, column)
        
        # Отрисовка препятствий
        for wall in self.walls:
            self.draw_block(screen, COLORS['WALL'], wall.x, wall.y)
        
        # Отрисовка еды
        if self.food:
            self.draw_block(screen, COLORS['FOOD'], self.food.x, self.food.y)
        
        # Отрисовка яда
        if self.poison:
            self.draw_block(screen, COLORS['POISON'], self.poison.x, self.poison.y)
        
        # Отрисовка бонуса
        if self.bonus:
            # Проверяем, не истек ли бонус
            if self.bonus.is_expired():
                self.bonus = None
            else:
                self.draw_block(screen, COLORS['BONUS'], self.bonus.x, self.bonus.y)
        
        # Отрисовка змеи
        for i, block in enumerate(self.snake_blocks):
            color = (255, 255, 255) if i == len(self.snake_blocks) - 1 else self.settings.snake_color
            self.draw_block(screen, color, block.x, block.y)
        
        # Отрисовка щита
        if self.shield_active:
            head = self.snake_blocks[-1]
            shield_rect = pygame.Rect(
                SIZE_BLOCK + head.y * SIZE_BLOCK + MARGIN * (head.y + 1),
                HEADER_MARGIN + SIZE_BLOCK + head.x * SIZE_BLOCK + MARGIN * (head.x + 1),
                SIZE_BLOCK, SIZE_BLOCK
            )
            pygame.draw.rect(screen, COLORS['SHIELD'], shield_rect, 3)
        
        # Текст
        text_total = font.render(f"Score: {self.total}", 0, COLORS['PINK'])
        text_level = font.render(f"Level: {self.level}", 0, COLORS['PINK'])
        text_best = font.render(f"Best: {self.personal_best}", 0, COLORS['PINK'])
        
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_level, (SIZE_BLOCK + 200, SIZE_BLOCK))
        screen.blit(text_best, (SIZE_BLOCK + 400, SIZE_BLOCK))
        
        if self.bonus_effect_active:
            effect_text = font.render(f"Bonus: {self.bonus_effect_active}", 0, COLORS['BONUS'])
            screen.blit(effect_text, (SIZE_BLOCK + 600, SIZE_BLOCK))
    
    def draw_block(self, screen, color, row, column):
        pygame.draw.rect(screen, color,
                        [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                         HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                         SIZE_BLOCK, SIZE_BLOCK])
    
    def save_result(self):
        self.db.save_game_result(self.username, self.total, self.level)
    
    def close(self):
        self.db.close()