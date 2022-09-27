import math
import random
import tkinter as tk
from collections import Counter

import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as sta

from . import config
from .exceptions import ValidationError


class Task1Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        tk.Label(
            self,
            text="Генератор непрерывного равномерного распределения на интервале (a, b) методом обратных функций",
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

        if value_a > value_b:
            self.set_error_message(self.header_label_a, "a should be less than b")
            return

        data = self.generate(value_a, value_b)
        self.show_actual_point_estimate(data)
        self.show_theoretical_point_estimate(value_a, value_b)
        self.show_actual_interval_estimate(data)
        self.show_theoretical_interval_estimate(value_a, value_b)
        self.show_listbox_report(data)
        self.show_method(value_a, value_b)
        self.show_histogram_report(data)

    @staticmethod
    def generate(a, b):
        data = list()
        for _ in range(config.n):
            data.append(Task1Frame.f(a, b))
        return data

    @staticmethod
    def f(a, b, r=None):
        """
        Интеграл dx / (b - a) от a до x это (x - a) / (b - a) = r
        отсюда x = (b - a) * r + a
        r распределен равномерно на промежутке [0, 1)
        https://mydocx.ru/2-119450.html
        """
        if r is None:
            r = random.random()
        return (b - a) * r + a

    def show_listbox_report(self, data):
        tk.Label(self, text="Generated data:").grid(row=3, column=0, rowspan=2)
        listbox = tk.Listbox(self)
        sorted_data = sorted(data)
        [
            listbox.insert(tk.END, e)
            for e in sorted_data[:20] + ['...'] + sorted_data[-20:]
        ]
        listbox.grid(row=3, column=1, rowspan=2)

    def show_method(self, value_a, value_b):
        fig, ax = plt.subplots()
        x = [random.random() for i in range(10)]
        y = [self.f(value_a, value_b, xi) for xi in x]
        ax.scatter(x, y)
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)  #  ширина Figure
        fig.set_figheight(6)  #  высота Figure

        plt.show()

    def show_histogram_report(self, data):
        fig, ax = plt.subplots()
        counter = Counter([math.floor(e) + 0.5 for e in data])
        ax.bar(counter.keys(), counter.values())

        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)  #  ширина Figure
        fig.set_figheight(6)  #  высота Figure

        plt.show()

    def show_actual_point_estimate(self, data):
        tk.Label(self, text="Actual point estimate M[X]:").grid(row=5, column=0)
        tk.Label(self, text=f"{self.get_actual_mx(data)}").grid(row=5, column=1)

        tk.Label(self, text="Actual point estimate D[X]:").grid(row=6, column=0)
        tk.Label(self, text=f"{self.get_actual_disp(data)}").grid(row=6, column=1)

    def show_theoretical_point_estimate(self, a, b):
        """
        p(x) = 1 / (a + b) при x на [a, b]
        M[X] - Интеграл x * p(x) от a до b
        D[X] - интеграл x^2 * p(x) от a до b
        http://old.gsu.by/biglib/GSU/%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9/%D0%AD%D0%9A%D0%B8%D0%A2%D0%92/%D1%80%D1%83%D0%BA-%D0%BB%D0%B0%D0%B1-%D0%9C%D0%A1/2%20%D0%A1%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B8%20%D0%BD%D0%B5%D0%B8%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D0%BE%D0%B2.pdf
        """
        tk.Label(self, text="Theoretical point estimate M[X]:").grid(row=7, column=0)
        tk.Label(self, text=f"{(a + b) / 2}").grid(row=7, column=1)

        tk.Label(self, text="Theoretical point estimate D[X]:").grid(row=8, column=0)
        tk.Label(self, text=f"{(a ** 2 + a * b + b ** 2) / 3}").grid(row=8, column=1)

    def show_actual_interval_estimate(self, data, n=1000, confidence_level=0.95):
        """
        http://old.gsu.by/biglib/GSU/%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9/%D0%AD%D0%9A%D0%B8%D0%A2%D0%92/%D1%80%D1%83%D0%BA-%D0%BB%D0%B0%D0%B1-%D0%9C%D0%A1/3%20%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B8%20%D0%BD%D0%B5%D0%B8%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D0%BE%D0%B2.pdf
        """
        # from laplace
        normal_quantile = sta.norm.ppf((1 + confidence_level) / 2)
        sample_mean = self.get_actual_mx(data)
        sample_disp = self.get_actual_disp(data)

        left = sample_mean - math.sqrt(sample_disp / n) * normal_quantile
        right = sample_mean + math.sqrt(sample_disp / n) * normal_quantile

        tk.Label(
            self,
            text=f"Actual interval estimate M[X] with confidence level={confidence_level}:",
        ).grid(row=9, column=0)
        tk.Label(self, text=f"[{left}, {right}]").grid(row=9, column=1)

        chi_mass = sta.chi2(n - 1)
        array = chi_mass.rvs(config.n)
        temp = sta.mstats.mquantiles(
            array, prob=[(1 - confidence_level) / 2, (1 + confidence_level) / 2]
        )
        xi_minus = temp[1]
        xi_plus = temp[0]
        left = (n - 1) * sample_disp / xi_minus
        right = (n - 1) * sample_disp / xi_plus

        tk.Label(
            self,
            text=f"Actual interval estimate D[X] with confidence level={confidence_level}:",
        ).grid(row=10, column=0)
        tk.Label(self, text=f"[{left}, {right}]").grid(row=10, column=1)

    def show_theoretical_interval_estimate(self, a, b, confidence_level=0.95):
        pass

    def get_actual_mx(self, data):
        return sum(data) / len(data)

    def get_actual_disp(self, data):
        return sum([e**2 for e in data]) / len(data)
