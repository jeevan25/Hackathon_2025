# global_store.py

class globalStore:
    ai_output = None

    def store_ai_output(self,value):
        global _ai_output
        self.ai_output = value

    def get_ai_output(self):
        return self.ai_output