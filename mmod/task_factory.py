import tkinter as tk

from .task1 import Task1Frame


class TaskFactory:
    def create_task(self, task_name) -> tk.Frame:
        if task_name == 'task1':
            return Task1Frame

        raise NotImplementedError(f'Task {task_name} was not implemented')
