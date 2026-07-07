from todo_task import Task

class Task_Manager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        if not title.strip():
            print("Task cannot be empty.")
            return

        task = Task(title)
        self.tasks.append(task)
        
    def view_tasks(self):
        if not self.tasks:
            print("You Have No Tasks")
        else:
            for index, task in enumerate(self.tasks, start = 1):
                print(f"{index}, {task}")

    def complete_task(self, usr_input):
        if not usr_input.isdigit():
            print("Please enter a whole number.")
            return

        task_number = int(usr_input)
        target_index = task_number - 1

        if 0 <= target_index < len(self.tasks):
            self.tasks[target_index].mark_completed()
            print(f"Task {task_number} marked as completed.")
        else:
            print(f"Error: Task {task_number} does not exist. There are only {len(self.tasks)} tasks.")

    def delete_task(self, usr_input_d):

        if not usr_input_d.isdigit():
            print("Please enter a whole number.")
            return
        
        task_number = int(usr_input_d)
        target_index = task_number - 1

        if 0 <= target_index < len(self.tasks):
            deleted_task = self.tasks.pop(target_index)
            print(f"Succesfully Deleted: '{deleted_task}'")
            print(f"Remaining Tasks: {len(self.tasks)}")

        else:
            print(f"Error: Task {task_number} does not exist. There are only {len(self.tasks)} tasks.")

    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            for task in self.tasks:
                status = 1 if task.completed else 0
            f.write(f"{status}|{task.title}\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                self.tasks = []
