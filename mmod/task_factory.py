import tkinter as tk

from .task1 import Task1Frame
from .task2 import Task2Frame
from .task3 import Task3Frame
from .task4 import Task4Frame


class TaskFactory:
    @staticmethod
    def create_task(task_name) -> tk.Frame:
        if task_name == "task1":
            return Task1Frame
        elif task_name == 'task2':
            return Task2Frame
        elif task_name == 'task3':
            return Task3Frame
        elif task_name == 'task4':
            return Task4Frame

        raise NotImplementedError(f"Task {task_name} was not implemented")
