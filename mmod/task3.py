import random
import tkinter as tk

from . import config
from .exceptions import ValidationError


class Task3Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.header_label1 = tk.Label(self, fg='red')
        self.header_label1.grid(row=0, column=1)

        tk.Label(self, text='Input P(A): ').grid(row=1, column=0)
        self.entry1 = tk.Entry(self)
        self.entry1.bind('<Return>', self.on_submit)
        self.entry1.grid(row=1, column=1, padx=5, pady=5)

        self.header_label2 = tk.Label(self, fg='red')
        self.header_label2.grid(row=0, column=3)

        tk.Label(self, text='Input P(B|A): ').grid(row=1, column=2)
        self.entry2 = tk.Entry(self)
        self.entry2.bind('<Return>', self.on_submit)
        self.entry2.grid(row=1, column=3, padx=5, pady=5)

        self.report_labels = list()

    def set_error_message(self, info_label, err_message):
        info_label['text'] = err_message

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

    def on_submit(self, ev):
        value1 = self.entry1.get()

        self.set_error_message(self.header_label1, '')
        try:
            probability1 = self.validate_is_probability(self.header_label1, value1)
        except ValidationError:
            return

        value2 = self.entry2.get()

        self.set_error_message(self.header_label2, '')
        try:
            probability2 = self.validate_is_probability(self.header_label2, value2)
        except ValidationError:
            return

        data = self.generate(probability1, probability2)
        self.destroy_report_lables()
        self.show_actual_report(data)
        self.show_theoretical_report(probability1, probability2)

    def generate(self, probability1: float, probability2: float):
        data = list()
        for _ in range(config.n):
            is_a_happened = random.random() <= probability1
            if is_a_happened:
                is_b_happened = random.random() <= probability2
            else:
                is_b_happened = random.random() <= 1 - probability2

            if is_a_happened and is_b_happened:
                res = 0
            elif is_a_happened and not is_b_happened:
                res = 1
            elif not is_a_happened and is_b_happened:
                res = 2
            elif not is_a_happened and not is_b_happened:
                res = 3

            data.append(res)
        return data

    def destroy_report_lables(self):
        for label in self.report_labels:
            label.destroy()
        self.report_labels.clear()

    def show_actual_report(self, data):
        for i, el in enumerate(sorted(set(data))):
            label = tk.Label(self, text=f'Actual {el} events:')
            label.grid(row=i + 2, column=0)
            self.report_labels.append(label)

            label = tk.Label(self, text=f'{data.count(el) / config.n * 100:.4f}%')
            label.grid(row=i + 2, column=1)
            self.report_labels.append(label)

    def show_theoretical_report(self, probability1: float, probability2: float):
        label = tk.Label(self, text='Theoretical 0 events:')
        label.grid(row=6, column=0)
        self.report_labels.append(label)
        label = tk.Label(self, text=f'{probability1 * probability2 * 100:.4f}%')
        label.grid(row=6, column=1)
        self.report_labels.append(label)

        label = tk.Label(self, text='Theoretical 1 events:')
        label.grid(row=7, column=0)
        self.report_labels.append(label)
        label = tk.Label(self, text=f'{probability1 * (1-probability2) * 100:.4f}%')
        label.grid(row=7, column=1)
        self.report_labels.append(label)

        label = tk.Label(self, text='Theoretical 2 events:')
        label.grid(row=8, column=0)
        self.report_labels.append(label)
        label = tk.Label(self, text=f'{(1-probability1) * (1-probability2) * 100:.4f}%')
        label.grid(row=8, column=1)
        self.report_labels.append(label)

        label = tk.Label(self, text='Theoretical 3 events:')
        label.grid(row=9, column=0)
        self.report_labels.append(label)
        label = tk.Label(
            self, text=f'{(1-probability1) * (1-(1-probability2)) * 100:.4f}%'
        )
        label.grid(row=9, column=1)
        self.report_labels.append(label)
