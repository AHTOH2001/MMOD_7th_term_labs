import tkinter as tk
from functools import partial

from .task_factory import TaskFactory


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        mainmenu = tk.Menu(self)
        self.config(menu=mainmenu)
        gomenu = tk.Menu(mainmenu, tearoff=0)
        gomenu.add_command(label="Back", command=self.destroy_current_frame)
        mainmenu.add_cascade(label="Go", menu=gomenu)
        self.columnconfigure(0, minsize=500)
        self.frame_stack = list()

    def destroy_current_frame(self):
        if len(self.frame_stack) > 1:
            frame = self.frame_stack.pop()
            frame.destroy()

    def init_tasks_buttons(self, tasks):
        frame = self.create_new_frame()
        for i, task_name in enumerate(tasks):
            button = tk.Button(
                frame, text=task_name, command=partial(self.init_task, task_name)
            )
            button.grid(row=i, padx=5, pady=10)

    def init_task(self, task_name):
        TaskFrame = TaskFactory.create_task(task_name)
        frame = self.create_new_frame()
        task_frame = TaskFrame(frame)
        task_frame.grid()

    def create_new_frame(self):
        if len(self.frame_stack) == 0:
            frame = tk.Frame(self)
        else:
            frame = tk.Frame(self.frame_stack[-1])
        frame.grid(row=0, columnspan=10, rowspan=10, sticky="NS")

        self.frame_stack.append(frame)
        return frame
