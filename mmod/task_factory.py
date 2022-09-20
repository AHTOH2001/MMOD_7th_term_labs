import tkinter as tk

from .task1 import Task1Frame
from .task2 import Task2Frame


class TaskFactory:
    @staticmethod
    def create_task(task_name) -> tk.Frame:
        if task_name == "task1":
            return Task1Frame
        elif task_name == 'task2':
            return Task2Frame

        raise NotImplementedError(f"Task {task_name} was not implemented")
