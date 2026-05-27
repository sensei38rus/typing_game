import pygame

class UI:
    def __init__(self, screen, font_large, font_medium):
        self.screen = screen
        self.font_large = font_large
        self.font_medium = font_medium
        self.width, self.height = screen.get_size()
        
    def draw_background(self):
        self.screen.fill((30, 30, 40))
        
    def draw_level_info(self, level_number, level_name, total_levels):
        
        text = self.font_medium.render(f"Уровень {level_number + 1}/{total_levels}: {level_name}", True, (200, 200, 200))
        x = self.width // 2 - text.get_width() // 2
        y = 20
        self.screen.blit(text, (x, y))
        
    def draw_starting_message(self, seconds):
        
       
        title = self.font_large.render("ПРИГОТОВИТЬСЯ", True, (255, 200, 100))
        title_x = self.width // 2 - title.get_width() // 2
        title_y = self.height // 3
        self.screen.blit(title, (title_x, title_y))
        
        
        timer_text = self.font_large.render(str(seconds), True, (255, 255, 255))
        timer_x = self.width // 2 - timer_text.get_width() // 2
        timer_y = self.height // 2
        self.screen.blit(timer_text, (timer_x, timer_y))
        
        
        hint = self.font_medium.render("Будьте готовы печатать...", True, (150, 150, 150))
        hint_x = self.width // 2 - hint.get_width() // 2
        hint_y = self.height // 2 + 80
        self.screen.blit(hint, (hint_x, hint_y))
        
    def draw_word(self, word):
        text = self.font_large.render(word, True, (255, 255, 255))
        x = self.width // 2 - text.get_width() // 2
        y = self.height // 3
        self.screen.blit(text, (x, y))
        
    def draw_user_input(self, user_input):
        display_text = user_input + "_"
        text = self.font_large.render(display_text, True, (200, 200, 100))
        x = self.width // 2 - text.get_width() // 2
        y = self.height // 2
        self.screen.blit(text, (x, y))
        
    def draw_timer_bar(self, remaining, total):
        ratio = remaining / total if total > 0 else 0
        bar_width = 400
        bar_height = 25
        x = self.width // 2 - bar_width // 2
        y = self.height - 100
        
        pygame.draw.rect(self.screen, (80, 80, 100), (x, y, bar_width, bar_height))
        
        if ratio > 0.5:
            color = (0, 200, 0)
        elif ratio > 0.2:
            color = (200, 200, 0)
        else:
            color = (200, 0, 0)
            
        pygame.draw.rect(self.screen, color, (x, y, int(bar_width * ratio), bar_height))
        
        time_text = self.font_medium.render(f"{remaining:.1f} сек", True, (255, 255, 255))
        self.screen.blit(time_text, (x + bar_width // 2 - time_text.get_width() // 2, y - 25))
        
    def draw_combo(self, combo):
        if combo > 1:
            text = self.font_medium.render(f"КОМБО x{combo}!", True, (255, 200, 0))
            x = self.width - 150
            y = 100
            self.screen.blit(text, (x, y))
            
    def draw_score(self, score):
        text = self.font_medium.render(f"Очки: {score}", True, (255, 255, 255))
        self.screen.blit(text, (20, 100))
        
    def draw_restart_message(self, seconds):
        
        text = self.font_large.render(f"ПЕРЕЗАПУСК... {seconds}", True, (255, 100, 100))
        x = self.width // 2 - text.get_width() // 2
        y = self.height // 2 + 100
        self.screen.blit(text, (x, y))
        
        hint = self.font_medium.render("Ошибка! Уровень начнется заново", True, (200, 200, 200))
        hint_x = self.width // 2 - hint.get_width() // 2
        self.screen.blit(hint, (hint_x, y + 50))
        
    def draw_level_complete(self):
        text = self.font_large.render("УРОВЕНЬ ПРОЙДЕН!", True, (100, 255, 100))
        x = self.width // 2 - text.get_width() // 2
        y = self.height // 2
        self.screen.blit(text, (x, y))
        
    def draw_game_over(self, score):
        self.screen.fill((0, 0, 0))
        text1 = self.font_large.render("ИГРА ПРОЙДЕНА!", True, (255, 255, 255))
        text2 = self.font_medium.render(f"Финальный счет: {score}", True, (200, 200, 200))
        text3 = self.font_medium.render("Нажмите ESC для выхода", True, (150, 150, 150))
        
        x1 = self.width // 2 - text1.get_width() // 2
        x2 = self.width // 2 - text2.get_width() // 2
        x3 = self.width // 2 - text3.get_width() // 2
        
        self.screen.blit(text1, (x1, self.height // 3))
        self.screen.blit(text2, (x2, self.height // 2))
        self.screen.blit(text3, (x3, self.height // 2 + 50))