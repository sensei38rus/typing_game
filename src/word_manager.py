import json
import os

class WordManager:
    def __init__(self, levels_folder="data/levels"):
        self.levels_folder = levels_folder
        self.levels = []
        self.load_all_levels()

    def load_all_levels(self):
        if not os.path.exists(self.levels_folder):
            self.create_default_levels()
            
        for filename in sorted(os.listdir(self.levels_folder)):
            if filename.endswith(".json"):
                with open(os.path.join(self.levels_folder, filename), 'r', encoding='utf-8') as f:
                    self.levels.append(json.load(f))

    def create_default_levels(self):
        os.makedirs(self.levels_folder, exist_ok=True)
        default_levels = [
            {"name": "Уровень 1 — Простые слова", "words": ["cat", "dog", "sun", "car", "book"]},
            {"name": "Уровень 2 — Длиннее", "words": ["house", "mouse", "green", "phone", "table"]},
            {"name": "Уровень 3 — Сложные", "words": ["programming", "university", "keyboard", "challenge", "python"]}
        ]
        for i, level in enumerate(default_levels):
            with open(f"{self.levels_folder}/level{i+1}.json", 'w', encoding='utf-8') as f:
                json.dump(level, f, ensure_ascii=False, indent=2)