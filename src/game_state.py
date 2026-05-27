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