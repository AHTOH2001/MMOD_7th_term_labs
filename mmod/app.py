import tkinter as tk
from contextlib import contextmanager
from tkinter import ttk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.title('Lab1')
        self.callbacks = {}
