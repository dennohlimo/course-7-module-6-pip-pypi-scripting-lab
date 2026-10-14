import json
import os
import sys

DATA_FILE = "tasks.json"


# Create the Task class
class Task:
    def __init__(self, task_id, title, completed=False):
        self.task_id = task_id
        self.title = title
        self.completed = completed

    # Mark a task as complete
    def complete(self):
        self.completed = True

    # Convert the task into a dictionary
    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "completed": self.completed
        }


# Create the User class
class User:
    def __init__(self, username):
        self.username = username
        self.tasks = []

    # Add a new task
    def add_task(self, title):
        task_id = len(self.tasks) + 1

        task = Task(task_id, title)
        self.tasks.append(task)

        return task

    # Mark a task as complete
    def complete_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                task.complete()
                return task

        raise ValueError("Task not found.")


# Create the TaskManager class
class TaskManager:
    def __init__(self):
        self.users = {}
        self.load_tasks()

    # Load saved tasks from the JSON file
    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            for user_data in data:
                username = user_data["username"]
                user = User(username)

                for task_data in user_data["tasks"]:
                    task = Task(
                        task_data["id"],
                        task_data["title"],
                        task_data["completed"]
                    )
                    user.tasks.append(task)

                self.users[username] = user

    # Save tasks to the JSON file
    def save_tasks(self):
        data = []

        for user in self.users.values():
            user_data = {
                "username": user.username,
                "tasks": []
            }

            for task in user.tasks:
                user_data["tasks"].append(task.to_dict())

            data.append(user_data)

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    # Find a user or create a new one
    def get_user(self, username, create=False):
        if username not in self.users:
            if create:
                self.users[username] = User(username)
            else:
                raise ValueError("User not found.")

        return self.users[username]

    # Export a user's tasks to a text file
    def export_tasks(self, username, filename):
        user = self.get_user(username)

        with open(filename, "w") as file:
            for task in user.tasks:
                if task.completed:
                    mark = "x"
                else:
                    mark = " "

                file.write(
                    f"[{mark}] {task.task_id}. {task.title}\n"
                )

        return filename


# Run the program
def main():
    if len(sys.argv) < 3:
        print("Please provide a command and username.")
        print("Commands: add-task, complete-task, list-tasks, export")
        return

    command = sys.argv[1]
    username = sys.argv[2]

    manager = TaskManager()

    try:
        # Add a task
        if command == "add-task":
            if len(sys.argv) < 4:
                print("Please provide a task title.")
                return

            title = " ".join(sys.argv[3:])
            user = manager.get_user(username, create=True)
            task = user.add_task(title)

            manager.save_tasks()

            print("Task added successfully!")
            print("Task ID:", task.task_id)
            print("Title:", task.title)

        # Complete a task
        elif command == "complete-task":
            if len(sys.argv) < 4:
                print("Please provide a task ID.")
                return

            task_id = int(sys.argv[3])

            user = manager.get_user(username)
            task = user.complete_task(task_id)

            manager.save_tasks()

            print("Task completed successfully!")
            print("Title:", task.title)

        # Display a user's tasks
        elif command == "list-tasks":
            user = manager.get_user(username)

            if len(user.tasks) == 0:
                print("This user has no tasks.")
            else:
                print("Tasks for", username)

                for task in user.tasks:
                    if task.completed:
                        status = "Completed"
                    else:
                        status = "Not completed"

                    print(
                        task.task_id,
                        "-",
                        task.title,
                        "-",
                        status
                    )

        # Export tasks
        elif command == "export":
            filename = "tasks.txt"

            if len(sys.argv) >= 5 and sys.argv[3] == "--output":
                filename = sys.argv[4]

            manager.export_tasks(username, filename)
            print("Tasks exported to", filename)

        else:
            print("Invalid command.")
            print("Commands: add-task, complete-task, list-tasks, export")

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()