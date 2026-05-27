import json
import os
from datetime import datetime

class Stats:
    def __init__(self, data_file="user_data/progress.json"):
        self.data_file = data_file
        self.successes = []
        self.fails = []
        self.final_score = 0
        self.load()
        
    def load(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.successes = data.get("successes", [])
                self.fails = data.get("fails", [])
                self.final_score = data.get("final_score", 0)
        else:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump({
                "successes": self.successes,
                "fails": self.fails,
                "final_score": self.final_score,
                "last_played": str(datetime.now())
            }, f, indent=2)
            
    def record_success(self, word):
        self.successes.append({"word": word, "time": str(datetime.now())})
        self.save()
        
    def record_fail(self, word):
        self.fails.append({"word": word, "time": str(datetime.now())})
        self.save()
        
    def save_final_score(self, score):
        self.final_score = score
        self.save()
        
    def get_accuracy(self):
        total = len(self.successes) + len(self.fails)
        if total == 0:
            return 100
        return len(self.successes) / total * 100
        
    def get_report(self):
        return {
            "total_success": len(self.successes),
            "total_fails": len(self.fails),
            "accuracy": self.get_accuracy(),
            "final_score": self.final_score
        }