import json
import os

class WordManager:
    def __init__(self, levels_folder="data/levels"):
        self.levels_folder = levels_folder
        self.levels = []
        self.load_all_levels()
        
   