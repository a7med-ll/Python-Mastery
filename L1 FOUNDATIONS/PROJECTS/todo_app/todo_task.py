class Task:
    def __init__(self, title : str, completed : bool = False):
        self.title = title
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        if not self.completed:
            return f"[ ] {self.title}"
        else:
            return f"[x] {self.title}"


