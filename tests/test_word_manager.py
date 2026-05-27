import json
from src.word_manager import WordManager

def test_word_manager_loads_existing_files(tmp_path):
    # Создаем временную директорию и файл уровня
    levels_dir = tmp_path / "levels"
    levels_dir.mkdir()
    level_file = levels_dir / "level1.json"
    
    test_data = {"name": "Test Level", "words": ["apple", "banana"]}
    level_file.write_text(json.dumps(test_data), encoding="utf-8")
    
    wm = WordManager(levels_folder=str(levels_dir))
    
    assert wm.get_level_count() == 1
    assert wm.get_level(0)["name"] == "Test Level"
    assert len(wm.get_level(0)["words"]) == 2

def test_word_manager_creates_defaults_if_empty(tmp_path):
    # Указываем пустую временную директорию
    empty_dir = tmp_path / "empty_levels"
    wm = WordManager(levels_folder=str(empty_dir))
    
    # Должны создаться 3 стандартных уровня
    assert wm.get_level_count() == 3
    assert wm.get_level(0)["name"] == "Уровень 1 — Простые слова"