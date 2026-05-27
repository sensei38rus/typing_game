import pygame
import time
import random

class GameState:
    def __init__(self, word_manager, stats, ui):
        self.word_manager = word_manager
        self.stats = stats
        self.ui = ui
        
        # Игровые переменные
        self.current_level = 0
        self.current_word_index = 0
        self.current_word = ""
        self.words = []
        self.original_words = []
        self.time_limit = 0
        self.start_time = 0
        self.remaining_time = 0
        self.user_input = ""
        self.combo = 1
        self.score = 0
        
        # Состояния: STARTING, PLAYING, RESTARTING, LEVEL_COMPLETE, GAME_OVER
        self.state = "STARTING"
        self.start_timer = 3  # 3 секунды до начала
        
        # Загружаем первый уровень (но слово пока не показываем)
        self.load_level_without_display(self.current_level)

    def load_level_without_display(self, level_idx):
        """Загружает уровень, но не показывает первое слово (для стартового экрана)"""
        level = self.word_manager.get_level(level_idx)
        if level:
            self.original_words = level["words"].copy()
            self.words = level["words"].copy()
            random.shuffle(self.words)
            self.current_word_index = 0
            self.combo = 1
            # Подготавливаем первое слово, но не показываем его
            self.prepare_first_word()
        else:
            self.state = "GAME_OVER"

    def prepare_first_word(self):
        """Подготавливает первое слово без отображения"""
        if self.current_word_index < len(self.words):
            self.current_word = self.words[self.current_word_index]
            self.time_limit = self.calculate_timeout(self.current_word)
            self.user_input = ""
            # Не показываем слово, пока не начнется игра
            self.show_word = False
        else:
            self.show_word = False

    def load_level(self, level_idx):
        """Загружает уровень и сразу показывает первое слово"""
        level = self.word_manager.get_level(level_idx)
        if level:
            self.original_words = level["words"].copy()
            self.words = level["words"].copy()
            random.shuffle(self.words)
            self.current_word_index = 0
            self.combo = 1
            self.next_word()
        else:
            self.state = "GAME_OVER"
            
    def restart_level(self):
        """Перезапуск текущего уровня с новым случайным порядком слов"""
        self.words = self.original_words.copy()
        random.shuffle(self.words)
        self.current_word_index = 0
        self.combo = 1
        self.next_word()

    def next_word(self):
        """Переход к следующему слову"""
        if self.current_word_index >= len(self.words):
            self.state = "LEVEL_COMPLETE"
            return
            
        self.current_word = self.words[self.current_word_index]
        self.time_limit = self.calculate_timeout(self.current_word)
        self.user_input = ""
        self.show_word = True  # Показываем слово
        
        if self.state == "PLAYING":
            self.start_time = time.time()
            self.remaining_time = self.time_limit
        else:
            self.remaining_time = self.time_limit

    def start_word_timer(self):
        """Запускает таймер для текущего слова"""
        self.start_time = time.time()
        self.remaining_time = self.time_limit
        
    def calculate_timeout(self, word):
        """Расчет времени на слово в зависимости от длины и комбо"""
        base = 1.5
        per_char = 0.3
        length = len(word)
        raw_time = base + (length * per_char)
        
        combo_penalty = 1.0 - (self.combo - 1) * 0.05
        combo_penalty = max(0.7, combo_penalty)
        
        timeout = raw_time * combo_penalty
        return max(1.0, round(timeout, 1))

    def handle_input(self, event):
        """Обработка ввода с клавиатуры"""
        if self.state != "PLAYING":
            return
            
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.check_answer()
        else:
            char = event.unicode
            if char.isprintable() and len(char) == 1:
                self.user_input += char
                
    def check_answer(self):
        """Проверка правильности введенного слова"""
        if self.user_input.strip().lower() == self.current_word.lower():
            # Успех!
            time_ratio = self.remaining_time / self.time_limit
            points = int(100 * self.combo * time_ratio)
            self.score += points
            self.combo += 1
            self.stats.record_success(self.current_word)
            self.current_word_index += 1
            self.next_word()
        else:
            # Ошибка!
            self.start_restart()
            
    def start_restart(self):
        """Перезапуск уровня из-за ошибки или таймаута"""
        self.state = "RESTARTING"
        self.restart_timer = 3
        self.stats.record_fail(self.current_word)
        
    def update(self, dt):
        """Обновление состояния игры"""
        if self.state == "STARTING":
            self.start_timer -= dt
            if self.start_timer <= 0:
                self.state = "PLAYING"
                # Теперь показываем первое слово и запускаем таймер
                self.show_word = True
                self.current_word = self.words[0]  # Берем первое слово
                self.time_limit = self.calculate_timeout(self.current_word)
                self.start_word_timer()
                
        elif self.state == "PLAYING":
            elapsed = time.time() - self.start_time
            self.remaining_time = max(0, self.time_limit - elapsed)
            
            if self.remaining_time <= 0:
                self.start_restart()
                
        elif self.state == "RESTARTING":
            self.restart_timer -= dt
            if self.restart_timer <= 0:
                self.state = "PLAYING"
                self.restart_level()
                self.start_word_timer()
                
        elif self.state == "LEVEL_COMPLETE":
            self.current_level += 1
            if self.current_level < self.word_manager.get_level_count():
                self.load_level(self.current_level)
                self.state = "STARTING"
                self.start_timer = 3
                self.show_word = False  # Прячем слово на стартовом экране
            else:
                self.state = "GAME_OVER"
                self.stats.save_final_score(self.score)