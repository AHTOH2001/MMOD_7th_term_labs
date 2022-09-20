import random
import tkinter as tk

from . import config
from .exceptions import ValidationError


class Task1Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.header_label = tk.Label(self, fg='red')
        self.header_label.grid(row=0, column=1)

        tk.Label(self, text='Input probability: ').grid(row=1, column=0)
        self.entry = tk.Entry(self)
        self.entry.bind('<Return>', self.on_submit)
        self.entry.grid(row=1, column=1, padx=5, pady=5)

    def set_error_message(self, err_message):
        self.header_label['text'] = err_message

    def validate_is_probability(self, value) -> float:
        try:
            value = float(value)
        except:
            self.set_error_message('Probability should be an integer')
            raise ValidationError()

        if not (0 <= value <= 1):
            self.set_error_message('Probability should be in between 0 and 1')
            raise ValidationError()

        return value

    def on_submit(self, ev):
        value = self.entry.get()
        self.set_error_message('')
        try:
            probability = self.validate_is_probability(value)
        except ValidationError:
            return

        data = self.generate(probability)
        self.show_actual_report(data)
        self.show_theoretical_report(probability)

    def generate(self, probability: float):
        data = list()
        for _ in range(config.n):
            val = random.random()
            data.append(val <= probability)
        return data

    def show_actual_report(self, data):
        tk.Label(self, text='Actual True events:').grid(row=2, column=0)
        tk.Label(self, text=f'{data.count(True) / config.n * 100:.4f}%').grid(
            row=2, column=1
        )

        tk.Label(self, text='Actual False events:').grid(row=3, column=0)
        tk.Label(self, text=f'{data.count(False) / config.n * 100:.4f}%').grid(
            row=3, column=1
        )

    def show_theoretical_report(self, probability):
        tk.Label(self, text='Theoretical True events:').grid(row=4, column=0)
        tk.Label(self, text=f'{probability * 100:.4f}%').grid(row=4, column=1)

        tk.Label(self, text='Theoretical False events:').grid(row=5, column=0)
        tk.Label(self, text=f'{(1 - probability) * 100:.4f}%').grid(row=5, column=1)
