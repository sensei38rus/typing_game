import threading
import time

class GameTimer:
    def __init__(self, duration, callback):
        self.duration = duration
        self.callback = callback
        self.remaining = duration
        self.running = False
        self.thread = None
        
    def start(self):
        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        
    def _run(self):
        while self.running:
            elapsed = time.time() - self.start_time
            self.remaining = max(0, self.duration - elapsed)
            if self.remaining <= 0:
                self.callback()
                break
            time.sleep(0.05)
            
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()