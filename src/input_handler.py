import pygame

class InputHandler:
    def __init__(self):
        self.current_input = ""
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            elif event.key == pygame.K_RETURN:
                answer = self.current_input
                self.current_input = ""
                return answer
            else:
                self.current_input += event.unicode
        return None
        
    def get_current_input(self):
        return self.current_input