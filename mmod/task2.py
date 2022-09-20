import random
import tkinter as tk

from . import config
from .exceptions import ValidationError


class Task2Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.header_label = tk.Label(self, fg='red')
        self.header_label.grid(row=0, column=1, columnspan=10)

        tk.Label(self, text='Input k: ').grid(row=1, column=0)
        self.entry_input_k = tk.Entry(self)
        self.entry_input_k.bind('<Return>', self.on_submit_input_k)
        self.entry_input_k.grid(row=1, column=1, padx=5, pady=5)

        self.label_columns: list[tk.Label] = list()
        self.entry_columns: list[tk.Entry] = list()

    def set_error_message(self, info_label, err_message):
        info_label['text'] = err_message

    def validate_is_pos_number(self, value) -> float:
        try:
            value = int(value)
        except:
            self.set_error_message(self.header_label, 'Should be an integer')
            raise ValidationError()

        if value <= 0:
            self.set_error_message(self.header_label, 'Should be positive')
            raise ValidationError()

        return value

    def on_submit_input_k(self, ev):
        value = self.entry_input_k.get()
        self.set_error_message(self.header_label, '')
        try:
            k = self.validate_is_pos_number(value)
        except ValidationError:
            return

        self.show_k_columns(k)

    def show_k_columns(self, k):

        tk.Label(self, text='Enter probabilities: ').grid(row=3, column=0)
        for entry in self.entry_columns:
            entry.destroy()
        self.entry_columns.clear()

        for label in self.label_columns:
            label.destroy()
        self.label_columns.clear()

        for i in range(k):
            entry = tk.Entry(self)
            entry.grid(row=3, column=i + 1)
            entry.bind('<Return>', self.on_submit_column)
            self.entry_columns.append(entry)

            label = tk.Label(self, fg='red')
            label.grid(row=2, column=i + 1)
            self.label_columns.append(label)

    def on_submit_column(self, ev):
        probabilities = list()
        for entry, label in zip(self.entry_columns, self.label_columns):
            self.set_error_message(label, '')
            value = entry.get()
            try:
                probability = self.validate_is_probability(label, value)
            except ValidationError:
                return
            probabilities.append(probability)

        data = self.generate(probabilities)
        self.show_actual_report(data)
        self.show_theoretical_report(probabilities)

    def validate_is_probability(self, info_label, value) -> float:
        try:
            value = float(value)
        except:
            self.set_error_message(info_label, 'Probability should be an integer')
            raise ValidationError()

        if not (0 <= value <= 1):
            self.set_error_message(
                info_label, 'Probability should be in between 0 and 1'
            )
            raise ValidationError()

        return value

    def generate(self, probabilities: list[float]):
        res = list()
        for probability in probabilities:
            data = list()
            for _ in range(config.n):
                val = random.random()
                data.append(val <= probability)
            res.append(data)
        return res

    def show_actual_report(self, data):
        tk.Label(self, text='Actual True events:').grid(row=4, column=0)
        tk.Label(self, text='Actual False events:').grid(row=5, column=0)
        for i, column_data in enumerate(data):
            tk.Label(
                self, text=f'{column_data.count(True) / config.n * 100:.4f}%'
            ).grid(row=4, column=i + 1)
            tk.Label(
                self, text=f'{column_data.count(False) / config.n * 100:.4f}%'
            ).grid(row=5, column=i + 1)

    def show_theoretical_report(self, probabilities):
        tk.Label(self, text='Theoretical True events:').grid(row=6, column=0)
        tk.Label(self, text='Actual False events:').grid(row=7, column=0)
        for i, probability in enumerate(probabilities):
            tk.Label(self, text=f'{probability * 100:.4f}%').grid(row=6, column=i + 1)
            tk.Label(self, text=f'{(1 - probability) * 100:.4f}%').grid(
                row=7, column=i + 1
            )
