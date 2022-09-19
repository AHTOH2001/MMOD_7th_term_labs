import tkinter as tk
from functools import partial

from .task_factory import TaskFactory


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.columnconfigure(0, minsize=250)

    def init_gui(self, tasks):
        for i, task_name in enumerate(tasks):
            button = tk.Button(
                self, text=task_name, command=partial(self.init_task, task_name)
            )
            button.grid(row=i, padx=5, pady=10)

    def init_task(self, task_name):
        task_factory = TaskFactory()
        TaskFrame = task_factory.create_task(task_name)

        for widget in self.winfo_children():
            widget.destroy()

        task_frame = TaskFrame(self)
        task_frame.pack()
