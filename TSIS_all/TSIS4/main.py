import pygame
import sys
from game import Game
from config import Settings, COLORS, size, HEADER_MARGIN, SIZE_BLOCK
from db import Database

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
    
    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
        
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, COLORS['FRAME'], self.rect, 2)
        
        text_surface = font.render(self.text, True, COLORS['FRAME'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Snake Game - Advanced")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('courier', 36)
        self.small_font = pygame.font.SysFont('courier', 24)
        self.settings = Settings()
        self.db = Database()
        self.username = ""
        self.input_active = False
        self.input_text = ""
    
    def draw_text_input(self, screen):
        prompt = self.small_font.render("Enter your username:", True, COLORS['PINK'])
        screen.blit(prompt, (size[0]//2 - 100, size[1]//2 - 100))
        
        input_rect = pygame.Rect(size[0]//2 - 100, size[1]//2 - 50, 200, 40)
        color = COLORS['PINK'] if self.input_active else COLORS['BLUE']
        pygame.draw.rect(screen, color, input_rect, 2)
        
        text_surface = self.small_font.render(self.input_text, True, COLORS['PINK'])
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        
        if self.input_active:
            pygame.draw.line(screen, COLORS['PINK'],
                           (input_rect.x + text_surface.get_width() + 5, input_rect.y + 5),
                           (input_rect.x + text_surface.get_width() + 5, input_rect.y + 35), 2)
    
    def main_menu(self):
        play_button = Button(size[0]//2 - 100, size[1]//2 - 60, 200, 50, 
                            "Play", COLORS['PINK'], COLORS['BLUE'])
        leaderboard_button = Button(size[0]//2 - 100, size[1]//2, 200, 50,
                                   "Leaderboard", COLORS['PINK'], COLORS['BLUE'])
        settings_button = Button(size[0]//2 - 100, size[1]//2 + 60, 200, 50,
                                "Settings", COLORS['PINK'], COLORS['BLUE'])
        quit_button = Button(size[0]//2 - 100, size[1]//2 + 120, 200, 50,
                            "Quit", COLORS['PINK'], COLORS['BLUE'])
        
        while True:
            self.screen.fill(COLORS['FRAME'])
            
            # Запрос имени пользователя
            if not self.username:
                self.draw_text_input(self.screen)
            else:
                title = self.font.render("SNAKE GAME", True, COLORS['PINK'])
                title_rect = title.get_rect(center=(size[0]//2, size[1]//2 - 150))
                self.screen.blit(title, title_rect)
                
                user_text = self.small_font.render(f"Player: {self.username}", True, COLORS['PINK'])
                self.screen.blit(user_text, (size[0]//2 - 50, size[1]//2 - 200))
                
                play_button.draw(self.screen, self.font)
                leaderboard_button.draw(self.screen, self.font)
                settings_button.draw(self.screen, self.font)
                quit_button.draw(self.screen, self.font)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                
                if not self.username:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        input_rect = pygame.Rect(size[0]//2 - 100, size[1]//2 - 50, 200, 40)
                        self.input_active = input_rect.collidepoint(event.pos)
                    
                    elif event.type == pygame.KEYDOWN and self.input_active:
                        if event.key == pygame.K_RETURN and self.input_text:
                            self.username = self.input_text
                            self.input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            if len(self.input_text) < 20:
                                self.input_text += event.unicode
                else:
                    if play_button.is_clicked(event):
                        self.start_game()
                    elif leaderboard_button.is_clicked(event):
                        self.show_leaderboard()
                    elif settings_button.is_clicked(event):
                        self.settings_menu()
                    elif quit_button.is_clicked(event):
                        self.db.close()
                        pygame.quit()
                        sys.exit()
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def start_game(self):
        game = Game(self.username, self.settings)
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.save_result()
                    game.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and game.d_row != 1:
                        game.d_row = -1
                        game.d_col = 0
                    elif event.key == pygame.K_DOWN and game.d_row != -1:
                        game.d_row = 1
                        game.d_col = 0
                    elif event.key == pygame.K_LEFT and game.d_col != 1:
                        game.d_row = 0
                        game.d_col = -1
                    elif event.key == pygame.K_RIGHT and game.d_col != -1:
                        game.d_row = 0
                        game.d_col = 1
            
            # Обновление игры
            if not game.move_snake():
                game.save_result()
                self.game_over(game.total, game.level, game.personal_best)
                running = False
            
            # Проверка истечения бонуса
            game.check_bonus_expiry()
            
            # Генерация нового бонуса
            if game.bonus is None and random.random() < 0.01:
                game.generate_bonus()
            
            # Отрисовка
            game.draw(self.screen, self.font)
            pygame.display.flip()
            game.clock.tick(game.update_speed())
        
        game.close()
    
    def game_over(self, score, level, best):
        retry_button = Button(size[0]//2 - 100, size[1]//2 + 20, 200, 50,
                             "Play Again", COLORS['PINK'], COLORS['BLUE'])
        menu_button = Button(size[0]//2 - 100, size[1]//2 + 80, 200, 50,
                            "Main Menu", COLORS['PINK'], COLORS['BLUE'])
        
        waiting = True
        while waiting:
            self.screen.fill(COLORS['FRAME'])
            
            game_over_text = self.font.render("GAME OVER", True, COLORS['PINK'])
            score_text = self.small_font.render(f"Score: {score}", True, COLORS['PINK'])
            level_text = self.small_font.render(f"Level: {level}", True, COLORS['PINK'])
            best_text = self.small_font.render(f"Best: {best}", True, COLORS['PINK'])
            
            game_over_rect = game_over_text.get_rect(center=(size[0]//2, size[1]//2 - 100))
            score_rect = score_text.get_rect(center=(size[0]//2, size[1]//2 - 40))
            level_rect = level_text.get_rect(center=(size[0]//2, size[1]//2))
            best_rect = best_text.get_rect(center=(size[0]//2, size[1]//2 + 40))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(level_text, level_rect)
            self.screen.blit(best_text, best_rect)
            
            retry_button.draw(self.screen, self.font)
            menu_button.draw(self.screen, self.font)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                elif retry_button.is_clicked(event):
                    self.start_game()
                    waiting = False
                elif menu_button.is_clicked(event):
                    waiting = False
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def show_leaderboard(self):
        top_scores = self.db.get_top_scores(10)
        back_button = Button(size[0]//2 - 100, size[1] - 100, 200, 50,
                            "Back", COLORS['PINK'], COLORS['BLUE'])
        
        waiting = True
        while waiting:
            self.screen.fill(COLORS['FRAME'])
            
            title = self.font.render("TOP 10 PLAYERS", True, COLORS['PINK'])
            title_rect = title.get_rect(center=(size[0]//2, 50))
            self.screen.blit(title, title_rect)
            
            y_offset = 120
            for i, (username, score, level, played_at) in enumerate(top_scores):
                text = f"{i+1}. {username} - Score: {score} - Level: {level}"
                score_text = self.small_font.render(text, True, COLORS['PINK'])
                self.screen.blit(score_text, (size[0]//2 - 200, y_offset))
                y_offset += 40
                
                if y_offset > size[1] - 150:
                    break
            
            back_button.draw(self.screen, self.font)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                elif back_button.is_clicked(event):
                    waiting = False
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def settings_menu(self):
        colors = [(255,255,255), (255,0,0), (0,255,0), (0,0,255), (255,255,0)]
        color_names = ["White", "Red", "Green", "Blue", "Yellow"]
        current_color_index = 0
        
        # Находим текущий цвет
        for i, color in enumerate(colors):
            if color == self.settings.snake_color:
                current_color_index = i
                break
        
        back_button = Button(size[0]//2 - 100, size[1] - 100, 200, 50,
                            "Save & Back", COLORS['PINK'], COLORS['BLUE'])
        
        waiting = True
        while waiting:
            self.screen.fill(COLORS['FRAME'])
            
            title = self.font.render("SETTINGS", True, COLORS['PINK'])
            title_rect = title.get_rect(center=(size[0]//2, 50))
            self.screen.blit(title, title_rect)
            
            # Настройка цвета
            color_text = self.small_font.render(f"Snake Color: {color_names[current_color_index]}", True, COLORS['PINK'])
            self.screen.blit(color_text, (size[0]//2 - 150, 150))
            
            # Кнопки изменения цвета
            prev_color = Button(size[0]//2 - 200, 200, 50, 40, "<", COLORS['PINK'], COLORS['BLUE'])
            next_color = Button(size[0]//2 + 150, 200, 50, 40, ">", COLORS['PINK'], COLORS['BLUE'])
            prev_color.draw(self.screen, self.small_font)
            next_color.draw(self.screen, self.small_font)
            
            # Показ текущего цвета
            color_preview = pygame.Rect(size[0]//2 - 50, 200, 100, 40)
            pygame.draw.rect(self.screen, colors[current_color_index], color_preview)
            
            # Настройка сетки
            grid_text = self.small_font.render(f"Show Grid: {'ON' if self.settings.show_grid else 'OFF'}", True, COLORS['PINK'])
            self.screen.blit(grid_text, (size[0]//2 - 150, 280))
            
            grid_toggle = Button(size[0]//2 + 100, 270, 80, 40, "Toggle", COLORS['PINK'], COLORS['BLUE'])
            grid_toggle.draw(self.screen, self.small_font)
            
            back_button.draw(self.screen, self.font)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                elif prev_color.is_clicked(event):
                    current_color_index = (current_color_index - 1) % len(colors)
                elif next_color.is_clicked(event):
                    current_color_index = (current_color_index + 1) % len(colors)
                elif grid_toggle.is_clicked(event):
                    self.settings.update(show_grid=not self.settings.show_grid)
                elif back_button.is_clicked(event):
                    self.settings.update(snake_color=colors[current_color_index])
                    waiting = False
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    import random
    menu = Menu()
    menu.main_menu()