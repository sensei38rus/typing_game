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
   