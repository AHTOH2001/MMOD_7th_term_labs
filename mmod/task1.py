import random
import tkinter as tk

from . import config
from .exceptions import ValidationError


class Task1Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        tk.Label(
            self,
            text="Генератор непрерывного* равномерного распределения на интервале (a, b) методом обратных функций",
        ).grid(row=0, column=0, columnspan=4)

        self.header_label_a = tk.Label(self, fg="red")
        self.header_label_a.grid(row=1, column=1)
        self.header_label_b = tk.Label(self, fg="red")
        self.header_label_b.grid(row=1, column=3)

        tk.Label(self, text="Input a: ").grid(row=2, column=0)
        self.entry_a = tk.Entry(self)
        self.entry_a.bind("<Return>", self.on_submit_ab)
        self.entry_a.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Input b: ").grid(row=2, column=2)
        self.entry_b = tk.Entry(self)
        self.entry_b.bind("<Return>", self.on_submit_ab)
        self.entry_b.grid(row=2, column=3, padx=5, pady=5)

    def set_error_message(self, info_label, err_message):
        info_label["text"] = err_message

    def validate_is_number(self, info_label, value) -> float:
        try:
            value = float(value)
        except:
            self.set_error_message(info_label, "Should be a number")
            raise ValidationError()

        return value

    def on_submit_ab(self, ev):
        value_a = self.entry_a.get()
        value_b = self.entry_b.get()
        self.set_error_message(self.header_label_a, "")
        self.set_error_message(self.header_label_b, "")

        try:
            value_a = self.validate_is_number(self.header_label_a, value_a)
            value_b = self.validate_is_number(self.header_label_b, value_b)
        except ValidationError:
            return

        data = self.generate(value_a, value_b)
        self.show_actual_report(data)
        # self.show_theoretical_report(probability)

    @staticmethod
    def generate(a, b):
        data = list()
        for _ in range(config.n):
            data.append(Task1Frame.f(a, b))
        return data

    @staticmethod
    def f(a, b):
        """
        Интеграл x / (b - a) от a до x это (x - a) / (b - a) = r
        отсюда x = (b - a) * r + a
        r распределен равномерно на промежутке [0, 1)
        """
        r = random.random()
        return (b - a) * r + a

    def show_actual_report(self, data):
        tk.Label(self, text="Generated data:").grid(row=3, column=0, rowspan=2)
        listbox = tk.Listbox(self)
        [listbox.insert(tk.END, e) for e in sorted(data)]
        listbox.grid(row=3, column=1, rowspan=2, columnspan=2)
        

    def show_theoretical_report(self, probability):
        tk.Label(self, text="Theoretical True events:").grid(row=4, column=0)
        tk.Label(self, text=f"{probability * 100:.4f}%").grid(row=4, column=1)

        tk.Label(self, text="Theoretical False events:").grid(row=5, column=0)
        tk.Label(self, text=f"{(1 - probability) * 100:.4f}%").grid(row=5, column=1)
