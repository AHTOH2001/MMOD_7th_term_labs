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

from . import config


class Task1Frame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.a, self.b = 0, pi / 2
        result = self.calculate()
        lbl = Label(self, text="f(x,y) = 0.5*sin(x+y)")
        lbl.grid(column=0, row=0)
        lbl = Label(self, text=f"0 <= x, y <= pi / 2")
        lbl.grid(column=0, row=1)

        btn = Button(
            self,
            text="Плотности распределения",
            command=partial(self.dens_info, result=result),
        )
        btn.grid(column=0, row=2)
        btn = Button(
            self,
            text="Графики",
            command=partial(
                self.graf,
                f=result["f"],
                fx=result["fx"],
                fy_x=result["fy_x"],
                res_y_big=result["res_y_big"],
                res_x_big=result["res_x_big"],
            ),
        )
        btn.grid(column=0, row=3)

        btn = Button(
            self,
            text="Фактические оценки",
            command=partial(
                self.get_real, res_y=result["res_y_big"], res_x=result["res_x_big"]
            ),
        )
        btn.grid(column=0, row=4)
        btn = Button(
            self,
            text="Теоретические оценки",
            command=partial(
                self.calc_teor,
                f=result["f"],
                res_y=result["res_y_big"],
                res_x=result["res_x_big"],
            ),
        )
        btn.grid(column=0, row=5)

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
                f"""
f(x|y):
{result['f(x|y)']}

f(y|x):
{result['f(y|x)']}
"""
            )

    def calc_teor(self, res_x, res_y, f, alpha=0.05):

        x, y = sp.symbols('x y')
        # xf(x)
        expn = "0.5*x*(sin(x)+cos(x))"
        a, b = 0, pi / 2
        m_x_t = sp.integrate(expn, (x, a, b))

        expn = "0.5*y*(sin(y)+cos(y))"
        m_y_t = sp.integrate(expn, (y, a, b))

        expn = "0.5*x*x*(sin(x)+cos(x))"
        d_x_t = sp.integrate(expn, (x, a, b)) - m_x_t**2

        expn = "0.5*y*y*(sin(y)+cos(y))"
        d_y_t = sp.integrate(expn, (y, a, b)) - m_y_t**2

        expn = f"(x-{m_x_t})*(y-{m_y_t})*0.5*sin(x+y)"
        cov = sp.integrate(expn, (x, a, b), (y, a, b))
        r_t = cov / (math.sqrt(d_x_t * d_y_t))

        s = (
            f"M : \n{[m_x_t, m_y_t]},"
            + "\n\n"
            + f" D: \n{[d_x_t, d_y_t]},"
            + "\n\n"
            + f"r: \n{[r_t]}"
            + "\n\n"
        )
        # messagebox.showinfo('theoritic',s)

        m_x = sum(res_x) / len(res_x)
        m_y = sum(res_y) / len(res_y)

        tmp_x = np.array(res_x) - m_x
        tmp_y = np.array(res_y) - m_y

        d_x = (tmp_x @ tmp_x) / (len(res_x) - 1)
        d_y = (tmp_y @ tmp_y) / (len(res_y) - 1)

        r = (tmp_x @ tmp_y) / (len(res_x) * np.sqrt(d_x * d_y))

        gamma = 1.0 - alpha
        delta_x = d_x * sta.t.ppf(gamma, len(res_x) - 1) / np.sqrt(len(res_x) - 1)
        delta_y = d_y * sta.t.ppf(gamma, len(res_y) - 1) / np.sqrt(len(res_y) - 1)

        lx = ((len(res_x) - 1) * d_x) / scipy.stats.chi2.ppf(
            1 - alpha / 2, len(res_x) - 1
        )
        rx = ((len(res_x) - 1) * d_x) / scipy.stats.chi2.ppf(alpha / 2, len(res_x) - 1)

        ly = ((len(res_y) - 1) * d_y) / scipy.stats.chi2.ppf(
            1 - alpha / 2, len(res_y) - 1
        )
        ry = ((len(res_y) - 1) * d_y) / scipy.stats.chi2.ppf(alpha / 2, len(res_y) - 1)

        r_scaled = np.arctanh(r)
        r_scaled_std = 1 / np.sqrt(len(res_x) - 3)
        z = scipy.stats.norm.ppf(1 - alpha / 2)
        rxy_l, rxy_r = np.tanh(r_scaled - z * r_scaled_std), np.tanh(
            r_scaled + z * r_scaled_std
        )

        s += (
            f"m_x_interval: \n{(round(m_x - delta_x, 5), round(m_x + delta_x, 5))},"
            + "\n\n"
        )
        s += (
            f"m_y interval: \n{(round(m_y - delta_y, 5), round(m_y + delta_y, 5))},"
            + "\n\n"
        )
        s += f"d_x interval: \n{(round(lx, 5), round(rx, 5))}," + "\n\n"
        s += f"d_y interval: \n{ (round(ly, 5), round(ry, 5))}," + "\n\n"
        s += f"r interval: \n{ (round(rxy_l, 5), round(rxy_r, 5))}," + "\n\n"
        messagebox.showinfo('both', s)

        # стьюдент
        n = len(res_x)
        diff = (m_x - m_x_t) * np.sqrt(n) / np.sqrt(d_x)
        critical_level = scipy.stats.t.ppf(alpha, n)
        ss = f"check mx: \n{diff < abs(critical_level)}"

        messagebox.showinfo('hypotesis', ss)

        n = len(res_y)
        diff = (m_y - m_y_t) * np.sqrt(n) / np.sqrt(d_y)
        critical_level = scipy.stats.t.ppf(alpha, n)
        ss = f"check my: \n{diff < abs(critical_level)}"

        messagebox.showinfo('hypotesis', ss)

        # хи квадрат
        n = len(res_x)

        chi2 = (n - 1) * d_x / d_x_t

        chi2_l = scipy.stats.chi2.ppf(alpha / 2, n - 1)
        chi2_r = scipy.stats.chi2.ppf(1 - 0.05 / 2, n - 1)

        ss = f"check dx: \n{chi2_l < chi2 < chi2_r}"

        messagebox.showinfo('hypotesis', ss)

        n = len(res_y)

        chi2 = (n - 1) * d_y / d_y_t

        chi2_l = scipy.stats.chi2.ppf(alpha / 2, n - 1)
        chi2_r = scipy.stats.chi2.ppf(1 - 0.05 / 2, n - 1)

        ss = f"check dy: \n{chi2_l < chi2 < chi2_r}"

        messagebox.showinfo('hypotesis', ss)

    def get_real(self, res_x, res_y, alpha=0.05):
        m_x = sum(res_x) / len(res_x)
        m_y = sum(res_y) / len(res_y)

        tmp_x = np.array(res_x) - m_x
        tmp_y = np.array(res_y) - m_y

        d_x = (tmp_x @ tmp_x) / (len(res_x) - 1)
        d_y = (tmp_y @ tmp_y) / (len(res_y) - 1)

        r = (tmp_x @ tmp_y) / (len(res_x) * np.sqrt(d_x * d_y))

        gamma = 1.0 - alpha
        delta_x = d_x * sta.t.ppf(gamma, len(res_x) - 1) / np.sqrt(len(res_x) - 1)
        delta_y = d_y * sta.t.ppf(gamma, len(res_y) - 1) / np.sqrt(len(res_y) - 1)

        lx = ((len(res_x) - 1) * d_x) / scipy.stats.chi2.ppf(
            1 - alpha / 2, len(res_x) - 1
        )
        rx = ((len(res_x) - 1) * d_x) / scipy.stats.chi2.ppf(alpha / 2, len(res_x) - 1)

        ly = ((len(res_y) - 1) * d_y) / scipy.stats.chi2.ppf(
            1 - alpha / 2, len(res_y) - 1
        )
        ry = ((len(res_y) - 1) * d_y) / scipy.stats.chi2.ppf(alpha / 2, len(res_y) - 1)

        r_scaled = np.arctanh(r)
        r_scaled_std = 1 / np.sqrt(len(res_x) - 3)
        z = scipy.stats.norm.ppf(1 - alpha / 2)
        rxy_l, rxy_r = np.tanh(r_scaled - z * r_scaled_std), np.tanh(
            r_scaled + z * r_scaled_std
        )

        s = (
            f"M : \n{[m_x, m_y]},"
            + "\n\n"
            + f" D: \n{[d_x, d_y]},"
            + "\n\n"
            + f"r: \n{[r]}"
            + "\n\n"
        )
        s += (
            f"m_x_interval: \n{(round(m_x - delta_x, 5), round(m_x + delta_x, 5))},"
            + "\n\n"
        )
        s += (
            f"m_y interval: \n{(round(m_y - delta_y, 5), round(m_y + delta_y, 5))},"
            + "\n\n"
        )
        s += f"d_x interval: \n{(round(lx, 5), round(rx, 5))}," + "\n\n"
        s += f"d_y interval: \n{ (round(ly, 5), round(ry, 5))}," + "\n\n"
        # s+= f"r interval: \n{ (round(rxy_l, 5), round(rxy_r, 5))}," +"\n\n"
        messagebox.showinfo('real', s)

        return {
            'M': [m_x, m_y],
            'D': [d_x, d_y],
            'r': [r],
            'm_x interval': (round(m_x - delta_x, 5), round(m_y + delta_x, 5)),
            'm_y interval': (round(m_x - delta_x, 5), round(m_y + delta_x, 5)),
            'd_x interval': (round(lx, 5), round(rx, 5)),
            'd_y interval': (round(ly, 5), round(ry, 5)),
            'r interval': (round(rxy_l, 5), round(rxy_r, 5)),
        }
