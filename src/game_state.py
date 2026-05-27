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

    