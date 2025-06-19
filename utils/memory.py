class ChatMemory:
    def __init__(self):
        self.history = []  # List of (question, answer)

    def add(self, question, answer):
        self.history.append((question, answer))

    def get(self):
        return self.history

    def clear(self):
        self.history = [] 