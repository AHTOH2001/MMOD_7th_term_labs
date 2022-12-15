import math
import random
from functools import partial
from math import pi
from tkinter import *
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats as sta
import sympy as sp

from .theor_frame import TheorFrame

from . import config


class Task1Frame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        lbl = Label(self, text="Тип СМО:")
        lbl.grid(column=0, row=0)
        lbl = Label(self, text="Одноканальное с ожиданием")
        lbl.grid(column=1, row=0)

        lbl = Label(self, text='Кол-во мест в очереди:')
        lbl.grid(column=0, row=1)
        self.m_entry = Entry(self)
        self.m_entry.insert(0, str(config.m))
        self.m_entry.grid(column=1, row=1)

        lbl = Label(self, text='Кол-во заявок в час:')
        lbl.grid(column=0, row=2)
        self.lambd_entry = Entry(self)
        self.lambd_entry.insert(0, str(config.lambd))
        self.lambd_entry.grid(column=1, row=2)

        lbl = Label(self, text='Поток восстановлений:')
        lbl.grid(column=0, row=3)
        self.mu_entry = Entry(self)
        self.mu_entry.insert(0, str(config.mu))
        self.mu_entry.grid(column=1, row=3)

        btn = Button(self, text="Теоретические оценки", command=self.calc_teor)
        btn.grid(column=0, row=4, columnspan=2)

        btn = Button(
            self,
            text="Моделирование",
        )
        btn.grid(column=0, row=5, columnspan=2)

        btn = Button(
            self,
            text="График",
        )
        btn.grid(column=0, row=6, columnspan=2)

    def parse_data(self):
        m = int(self.m_entry.get())
        lambd = int(self.lambd_entry.get())
        mu = float(self.mu_entry.get())
        print(f'Entered data: {m=}, {lambd=}, {mu=}')
        return m, lambd, mu

    def calc_teor(self):
        frame = self.master.master.create_new_frame(TheorFrame)
        frame.grid()        

    def my_hist(self, res, ff, fig, ax, color=None):
        bins = (int)(math.log10(100000) * 2)
        ls = np.linspace(np.min(res), np.max(res), 100)

        ax.cla()
        ax.hist(
            res,
            bins=bins,
            density=True,
            histtype='step',
            label='Empirical',
            color=color,
        )
        ax.plot(ls, [ff(i) for i in ls], color='red')
        ax.set_title('hist X')

    def my_hist_y(self, res_x, res_y, ff, fig, ax, color=None):
        bins = (int)(math.log10(100000) * 2)
        ls = np.linspace(np.min(res_y), np.max(res_y), 100)

        ax.cla()
        ax.hist(
            res_y,
            bins=bins,
            density=True,
            histtype='step',
            label='Empirical',
            color=color,
        )
        xx = sum(res_x) / len(res_x)
        res = []
        for i in ls:
            res.append(ff(xx, i))
        ax.plot(ls, res, color='red')
        ax.set_title('hist Y')
        # МЕТОД НЕЙМАНА

    def get_xyz(self, fx, fy_x, fy, W=math.sqrt(2) / 2, a=0, b=pi / 2, n=config.n):
        X = []
        Y = []
        # Z=[]

        for i in range(n):
            flag_x = False
            flag_y = False
            # x1_star=None
            while not flag_x:
                x1 = random.random()
                x2 = random.random()
                x1_star = a + x1 * (b - a)
                x2_star = x2 * W
                if fx(x1_star) >= x2_star:
                    X.append(x1_star)
                    # x1_star=x1_star
                    flag_x = True

            while not flag_y:
                # a_x=a_y
                y1 = random.random()
                y2 = random.random()
                y1_star = a + y1 * (b - a)
                y2_star = y2 * fy_x(x1_star)
                if fy(x1_star, y1_star) >= y2_star:
                    Y.append(y1_star)
                    flag_y = True
        return X, Y

    def calculate(self):
        np.random.seed(19680801)
        random.seed(19680801)
        result = {}
        x, y = sp.symbols('x y')
        expn = "0.5*sin(x+y)"

        gfg = sp.sympify(expn)
        f = sp.lambdify(sp.symbols('x, y'), expn)
        a, b = 0, pi / 2
        fy = sp.integrate(expn, (x, a, b))
        fx = sp.integrate(expn, (y, a, b))
        dep = sp.simplify(sp.Mul(fx, fy))
        ind_flag = dep.equals(expn)

        # условные вероятности
        fx_y = sp.simplify(gfg / fy)
        fy_x = sp.simplify(gfg / fx)
        result['f(x)'] = fx
        result['f(y)'] = fy
        result['f(x|y)'] = fx_y
        result['f(y|x)'] = fy_x
        fx = sp.lambdify(sp.symbols('x'), fx)
        fy = sp.lambdify(sp.symbols('y'), fy)
        fy_x = sp.lambdify(sp.symbols('x,y'), fy_x)

        def fy_x_max(x):
            return 1 / (math.sin(x) + math.cos(x))

        res_x_big, res_y_big = self.get_xyz(fx=fx, fy_x=fy_x_max, fy=fy_x, n=config.n)

        result['fx'] = fx
        result['fy'] = fy
        result['fy_x'] = fy_x
        result['f'] = f
        result['res_x_big'] = res_x_big
        result['res_y_big'] = res_y_big
        result["is_independant"] = ind_flag

        return result

    def graf(self, f, fx, fy_x, res_x_big, res_y_big):
        def fy_x_max(x):
            return 1 / (math.sin(x) + math.cos(x))

        fig, axes = plt.subplots(2, 1)

        self.my_hist(res_x_big, fx, fig, axes[0])
        self.my_hist_y(res_x_big, res_y_big, fy_x, fig, axes[1], color="green")
        plt.show()

        res_x, res_y = self.get_xyz(fx=fx, fy_x=fy_x_max, fy=fy_x, n=10000)

        fig = plt.figure()
        ax = plt.axes(projection='3d')

        x, y = np.array(res_x), np.array(res_y)
        hist, x_edges, y_edges = np.histogram2d(x, y, bins=10, density=True)

        x, y = np.meshgrid(x_edges[:-1], y_edges[:-1], indexing="ij")

        dx = dy = x_edges[1] - x_edges[0]

        dz = hist.ravel()

        ax.bar3d(x.ravel(), y.ravel(), 0, dx, dy, dz)

        ls1 = np.linspace(np.min(res_x), np.max(res_x), 1000)
        ls2 = np.linspace(np.min(res_y), np.max(res_y), 1000)
        ls1, ls2 = np.meshgrid(ls1, ls2)

        ax.plot_surface(
            ls1, ls2, np.array([f(*point) for point in zip(ls1, ls2)]), color="green"
        )
        plt.show()

    def dens_info(self, result):
        messagebox.showinfo(
            'Вероятности',
            f"""
f(x):
{result['f(x)']} 

f(y):
{result['f(y)']}
""",
        )
        if result["is_independant"]:
            messagebox.showinfo('Вероятности', "Независмы")
        else:
            messagebox.showinfo('Вероятности', "Зависмы")
            messagebox.showinfo(
                'Результат',
                f"""
f(x|y):
{result['f(x|y)']}

f(y|x):
{result['f(y|x)']}
""",
            )
