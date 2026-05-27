import pygame
import sys
from src.word_manager import WordManager
from src.ui import UI
from src.stats import Stats
from src.game_state import GameState

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Тренажер печати")
    
    font_large = pygame.font.SysFont("arial", 48)
    font_medium = pygame.font.SysFont("arial", 24)
    
    # Инициализация модулей
    word_manager = WordManager(levels_folder="data/levels")
    ui = UI(screen, font_large, font_medium)
    stats = Stats()
    
    game = GameState(word_manager, stats, ui)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Конвертация миллисекунд в секунды
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    game.handle_input(event)
                    
        game.update(dt)
        game.draw()
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()