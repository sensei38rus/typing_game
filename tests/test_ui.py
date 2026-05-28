import pytest
import pygame
from unittest.mock import Mock, patch
from src.ui import UI


@pytest.fixture
def mock_screen():
    """Create a mock pygame screen"""
    screen = Mock()
    screen.get_size.return_value = (800, 600)
    return screen


@pytest.fixture
def mock_fonts():
    """Create mock font objects"""
    font_large = Mock()
    font_medium = Mock()
    
    # Mock render method to return mock surfaces with width/height
    def mock_render(text, antialias, color):
        surface = Mock()
        surface.get_width.return_value = len(text) * 10  # Approximate width
        surface.get_height.return_value = 30
        return surface
    
    font_large.render.side_effect = mock_render
    font_medium.render.side_effect = mock_render
    
    return font_large, font_medium


@pytest.fixture
def ui(mock_screen, mock_fonts):
    """Create a UI instance with mocked dependencies"""
    font_large, font_medium = mock_fonts
    return UI(mock_screen, font_large, font_medium)


class TestUIInitialization:
    """Tests for UI class initialization"""
    
    def test_init_stores_attributes(self, ui, mock_screen, mock_fonts):
        """Test that UI stores screen and fonts correctly"""
        font_large, font_medium = mock_fonts
        assert ui.screen == mock_screen
        assert ui.font_large == font_large
        assert ui.font_medium == font_medium
        assert ui.width == 800
        assert ui.height == 600
    
    def test_init_gets_screen_size(self, mock_screen, mock_fonts):
        """Test that UI gets screen size on initialization"""
        font_large, font_medium = mock_fonts
        ui = UI(mock_screen, font_large, font_medium)
        mock_screen.get_size.assert_called_once()
        assert ui.width == 800
        assert ui.height == 600


class TestDrawBackground:
    """Tests for draw_background method"""
    
    def test_draw_background_fills_screen(self, ui):
        """Test that draw_background fills screen with correct color"""
        ui.draw_background()
        ui.screen.fill.assert_called_once_with((30, 30, 40))


class TestDrawLevelInfo:
    """Tests for draw_level_info method"""
    
    def test_draw_level_info_renders_correct_text(self, ui):
        """Test that level info renders with correct format"""
        ui.draw_level_info(0, "Easy Level", 5)
        
        # Check that render was called with correct text
        expected_text = "Уровень 1/5: Easy Level"
        ui.font_medium.render.assert_called_once_with(
            expected_text, True, (200, 200, 200)
        )
        
        # Check that blit was called
        assert ui.screen.blit.called
    
    def test_draw_level_info_with_different_level(self, ui):
        """Test level info with different level number"""
        ui.draw_level_info(3, "Hard Level", 10)
        
        expected_text = "Уровень 4/10: Hard Level"
        ui.font_medium.render.assert_called_once_with(
            expected_text, True, (200, 200, 200)
        )


class TestDrawStartingMessage:
    """Tests for draw_starting_message method"""
    
    def test_draw_starting_message_renders_all_components(self, ui):
        """Test that starting message renders title, timer and hint"""
        ui.draw_starting_message(3)
        
        # Check title was rendered
        ui.font_large.render.assert_any_call("ПРИГОТОВИТЬСЯ", True, (255, 200, 100))
        
        # Check timer was rendered
        ui.font_large.render.assert_any_call("3", True, (255, 255, 255))
        
        # Check hint was rendered
        ui.font_medium.render.assert_called_with(
            "Будьте готовы печатать...", True, (150, 150, 150)
        )
        
        # Check that blit was called 3 times (title, timer, hint)
        assert ui.screen.blit.call_count == 3
    
    def test_draw_starting_message_different_seconds(self, ui):
        """Test starting message with different seconds value"""
        ui.draw_starting_message(5)
        
        # Check timer was rendered with correct seconds
        ui.font_large.render.assert_any_call("5", True, (255, 255, 255))


class TestDrawWord:
    """Tests for draw_word method"""
    
    def test_draw_word_renders_word(self, ui):
        """Test that word is rendered correctly"""
        test_word = "Hello"
        ui.draw_word(test_word)
        
        ui.font_large.render.assert_called_once_with(
            test_word, True, (255, 255, 255)
        )
        assert ui.screen.blit.called
    
    def test_draw_word_empty_string(self, ui):
        """Test drawing empty word"""
        ui.draw_word("")
        
        ui.font_large.render.assert_called_once_with("", True, (255, 255, 255))


class TestDrawUserInput:
    """Tests for draw_user_input method"""
    
    def test_draw_user_input_with_text(self, ui):
        """Test that user input is rendered with cursor"""
        ui.draw_user_input("test")
        
        expected_text = "test_"
        ui.font_large.render.assert_called_once_with(
            expected_text, True, (200, 200, 100)
        )
        assert ui.screen.blit.called
    
    def test_draw_user_input_empty(self, ui):
        """Test drawing empty user input"""
        ui.draw_user_input("")
        
        expected_text = "_"
        ui.font_large.render.assert_called_once_with(
            expected_text, True, (200, 200, 100)
        )


class TestDrawTimerBar:
    """Tests for draw_timer_bar method"""
    
    def test_draw_timer_bar_full_time(self, ui):
        """Test drawing timer bar with full remaining time"""
        with patch('pygame.draw.rect') as mock_draw_rect:
            ui.draw_timer_bar(10.0, 10.0)
            
            # Should draw background and foreground rectangles
            assert mock_draw_rect.call_count == 2
            # Check that color is green for high ratio
            args = mock_draw_rect.call_args_list[1]
            assert args[0][1] == (0, 200, 0)
    
    def test_draw_timer_bar_half_time(self, ui):
        """Test drawing timer bar with half time remaining"""
        with patch('pygame.draw.rect') as mock_draw_rect:
            ui.draw_timer_bar(5.0, 10.0)
            
            args = mock_draw_rect.call_args_list[1]
            # Should be yellow for medium ratio
            assert args[0][1] == (200, 200, 0)
    
    def test_draw_timer_bar_low_time(self, ui):
        """Test drawing timer bar with low time remaining"""
        with patch('pygame.draw.rect') as mock_draw_rect:
            ui.draw_timer_bar(1.0, 10.0)
            
            args = mock_draw_rect.call_args_list[1]
            # Should be red for low ratio
            assert args[0][1] == (200, 0, 0)
    
    def test_draw_timer_bar_zero_total(self, ui):
        """Test drawing timer bar with zero total to avoid division by zero"""
        with patch('pygame.draw.rect') as mock_draw_rect:
            ui.draw_timer_bar(5.0, 0)
            
            # Should not crash, ratio becomes 0
            assert mock_draw_rect.call_count == 2
    
    def test_draw_timer_bar_renders_time_text(self, ui):
        """Test that timer bar renders time text"""
        ui.draw_timer_bar(5.5, 10.0)
        
        ui.font_medium.render.assert_called_with("5.5 сек", True, (255, 255, 255))


class TestDrawCombo:
    """Tests for draw_combo method"""
    
    def test_draw_combo_with_combo_greater_than_one(self, ui):
        """Test drawing combo when combo > 1"""
        ui.draw_combo(3)
        
        ui.font_medium.render.assert_called_once_with(
            "КОМБО x3!", True, (255, 200, 0)
        )
        assert ui.screen.blit.called
    
    def test_draw_combo_with_combo_equal_one(self, ui):
        """Test that combo is not drawn when combo == 1"""
        ui.draw_combo(1)
        
        ui.font_medium.render.assert_not_called()
        ui.screen.blit.assert_not_called()
    
    def test_draw_combo_with_combo_zero(self, ui):
        """Test that combo is not drawn when combo == 0"""
        ui.draw_combo(0)
        
        ui.font_medium.render.assert_not_called()


class TestDrawScore:
    """Tests for draw_score method"""
    
    def test_draw_score_renders_score(self, ui):
        """Test that score is rendered correctly"""
        ui.draw_score(150)
        
        ui.font_medium.render.assert_called_once_with(
            "Очки: 150", True, (255, 255, 255)
        )
        assert ui.screen.blit.called
    
    def test_draw_score_zero(self, ui):
        """Test drawing zero score"""
        ui.draw_score(0)
        
        ui.font_medium.render.assert_called_once_with(
            "Очки: 0", True, (255, 255, 255)
        )


class TestDrawRestartMessage:
    """Tests for draw_restart_message method"""
    
    def test_draw_restart_message_renders_all_components(self, ui):
        """Test that restart message renders both text lines"""
        ui.draw_restart_message(3)
        
        # Check main restart text
        ui.font_large.render.assert_called_once_with(
            "ПЕРЕЗАПУСК... 3", True, (255, 100, 100)
        )
        
        # Check hint text
        ui.font_medium.render.assert_called_once_with(
            "Ошибка! Уровень начнется заново", True, (200, 200, 200)
        )
        
        # Check that blit was called twice
        assert ui.screen.blit.call_count == 2
    
    def test_draw_restart_message_different_seconds(self, ui):
        """Test restart message with different seconds"""
        ui.draw_restart_message(5)
        
        ui.font_large.render.assert_called_once_with(
            "ПЕРЕЗАПУСК... 5", True, (255, 100, 100)
        )


class TestDrawLevelComplete:
    """Tests for draw_level_complete method"""
    
    def test_draw_level_complete_renders_message(self, ui):
        """Test that level complete message is rendered"""
        ui.draw_level_complete()
        
        ui.font_large.render.assert_called_once_with(
            "УРОВЕНЬ ПРОЙДЕН!", True, (100, 255, 100)
        )
        assert ui.screen.blit.called


class TestDrawGameOver:
    """Tests for draw_game_over method"""
    
    def test_draw_game_over_renders_all_components(self, ui):
        """Test that game over screen renders all text components"""
        ui.draw_game_over(500)
        
        # Check main title
        ui.font_large.render.assert_any_call(
            "ИГРА ПРОЙДЕНА!", True, (255, 255, 255)
        )
        
        # Check score text
        ui.font_medium.render.assert_any_call(
            "Финальный счет: 500", True, (200, 200, 200)
        )
        
        # Check exit instruction
        ui.font_medium.render.assert_any_call(
            "Нажмите ESC для выхода", True, (150, 150, 150)
        )
        
        # Check that screen fill was called
        ui.screen.fill.assert_called_once_with((0, 0, 0))
        
        # Check that blit was called 3 times
        assert ui.screen.blit.call_count == 3
    
    def test_draw_game_over_zero_score(self, ui):
        """Test game over screen with zero score"""
        ui.draw_game_over(0)
        
        ui.font_medium.render.assert_any_call(
            "Финальный счет: 0", True, (200, 200, 200)
        )


class TestIntegration:
    """Integration tests for multiple UI methods working together"""
    
    def test_draw_multiple_elements(self, ui):
        """Test drawing multiple UI elements in sequence"""
        ui.draw_background()
        ui.draw_score(100)
        ui.draw_word("Python")
        ui.draw_user_input("Py")
        
        assert ui.screen.fill.call_count == 1
        assert ui.font_medium.render.call_count == 1  # for score
        assert ui.font_large.render.call_count == 2  # for word and user input
    
    def test_timer_bar_color_changes_with_time(self, ui):
        """Test that timer bar color changes based on remaining time"""
        with patch('pygame.draw.rect') as mock_draw_rect:
            ui.draw_timer_bar(8.0, 10.0)  # 80% - green
            assert mock_draw_rect.call_args_list[1][0][1] == (0, 200, 0)
            
            ui.draw_timer_bar(3.0, 10.0)  # 30% - yellow
            assert mock_draw_rect.call_args_list[3][0][1] == (200, 200, 0)
            
            ui.draw_timer_bar(1.0, 10.0)  # 10% - red
            assert mock_draw_rect.call_args_list[5][0][1] == (200, 0, 0)