import tkinter as tk


class Task1Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        label = tk.Label(self, text="A")
        label.grid(row=0, column=0)
