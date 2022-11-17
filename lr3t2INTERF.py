from tkinter import *
from tkinter import ttk, messagebox

import math
import random
from collections import Counter
from math import pi
import scipy.stats as sta
import matplotlib
import matplotlib.pyplot as plt
import scipy
from scipy import integrate
import scipy.optimize as opt

print((11 - 1) % 9 + 1)
# 2

import sympy as sp
import numpy as np


# https://math.semestr.ru/math/system.php
def get_cond(data_p):
    n = data_p.shape[0]
    m = data_p.shape[1]

    res_xi_when_yj = np.zeros_like(data_p)
    res_yj_when_xi = np.zeros_like(data_p)
    for i in range(n):
        for j in range(m):
            res_xi_when_yj[i, j] = data_p[i, j] / np.sum(data_p[:, j])
            res_yj_when_xi[i, j] = data_p[i, j] / np.sum(data_p[i, :])

    return res_xi_when_yj, res_yj_when_xi

# def get_cond(data_p) :


def task2(alpha=0.05):
    data_p = entry.get()
    data_p=eval(data_p)
    data_p = np.array(data_p)

    n = data_p.shape[0]
    m = data_p.shape[1]


    # значения дсв
    x = np.array([i for i in range(data_p.shape[0])])
    y = np.array([i for i in range(data_p.shape[1])])
    messagebox.showinfo('значения дсв', f"значения дсв x={x}\n y={y}")

    p_x = np.sum(data_p, axis=1)
    print(x, p_x)
    # P(X=xi,Y=yk)=P(X=xi)⋅P(Y=yk),
    # https://www.matburo.ru/ex_tv.php?p1=tv2md
    print(np.sum(data_p))
    if np.sum(data_p) != 1:
        print("user durak")
        messagebox.showinfo('ошибка', "user durak")
        return

    else:
        # проверка независоимости
        flag = True
        for i in range(data_p.shape[0]):
            for j in range(data_p.shape[1]):
                if data_p[i, j] != np.sum(data_p[i, :]) * np.sum(data_p[:, j]):
                    flag = False
                    break
        if flag:
            print("Независимы")
            messagebox.showinfo('Независимы', "Независимы")

        else:
            print("Зависимы")
            messagebox.showinfo('Зависимы', "Зависимы")


        # # условные плотности
        res_xi_when_yj, res_yj_when_xi = get_cond(data_p)
        print(res_xi_when_yj)
        messagebox.showinfo('условные плотности', f"res_xi_when_yj = {res_xi_when_yj}\n\n res_yj_when_xi = {res_yj_when_xi}")

        # моделирование
        def gen_value_borders(p: list):
            value = random.random()
            section = 0.
            for i, p_i in enumerate(p):
                section += p_i
                if section > value:
                    return i

        def generate_d(p_x, res_yj_when_xi, n=10000):
            result = []

            for i in range(n):
                i = gen_value_borders(p_x)
                j = gen_value_borders(res_yj_when_xi[i])

                # добавляем значения
                result.append((x[i], y[j]))

            return result

        p_x = np.sum(data_p, axis=1)
        p_y = np.sum(data_p, axis=0)
        res = generate_d(p_x, res_yj_when_xi)
        # print(res)
        res_x = [el[0] for el in res]
        res_y = [el[1] for el in res]
        fig, axes = plt.subplots(2, 1)

        # ???????????
        # https://math.semestr.ru/math/system.php
        def get_theor(p_x, p_y, res, x, y):
            m_x = 0
            for i in range(len(x)):
                m_x += x[i] * p_x[i]

            m_y = 0
            for i in range(len(y)):
                m_y += y[i] * p_y[i]
            d_x_tmp = (x - m_x) ** 2
            d_x = d_x_tmp @ p_x
            d_y_tmp = (y - m_y) ** 2
            d_y = d_y_tmp @ p_y
            r = (x - m_x) @ ((y - m_y) @ data_p.T)
            r = r / np.sqrt(d_x * d_y)
            return {"mx": m_x,
                    "my": m_y,
                    "dx": d_x,
                    "dy": d_y,
                    "r": r
                    }

        th = get_theor(p_x, p_y, res, x, y)
        print(th)
        messagebox.showinfo('теоритические', f"{th}")

        # http://old.gsu.by/biglib/GSU/%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9/%D0%AD%D0%9A%D0%B8%D0%A2%D0%92/%D1%80%D1%83%D0%BA-%D0%BB%D0%B0%D0%B1-%D0%9C%D0%A1/3%20%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B8%20%D0%BD%D0%B5%D0%B8%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D0%BE%D0%B2.pdf
        def get_real(res_x, res_y, res, x, y):
            mx = sum(res_x) / len(res_x)
            my = sum(res_y) / len(res_y)

            tmp_x = res_x - mx
            tmp_y = res_y - my

            dx = (tmp_x @ tmp_x) / (len(res_x) - 1)
            dy = (tmp_y @ tmp_y) / (len(res_y) - 1)

            r = (tmp_x @ tmp_y) / (
                    len(res) * np.sqrt(dx * dy))
            return {"mx": mx,
                    "my": my,
                    "dx": dx,
                    "dy": dy,
                    "r": r
                    }

        real = get_real(res_x, res_y, res, x, y)
        print(real)
        messagebox.showinfo('практические', f"{real}")


        def my_hist(arr, fig, ax, k, color=None):
            counts = np.unique(arr, return_counts=True)[1]
            height = counts / counts.sum()
            osi = [i for i in range(k)]
            # ls = np.linspace(np.min(res), np.max(res), 100)
            ax.bar(x=osi, height=height, width=0.4, color=color)

        def my_hist_3d(res, x, y):
            np.random.seed(19680801)

            # fig = plt.figure()
            # ax = plt.axes(projection='3d')
            fig = plt.figure()
            ax = plt.axes(projection="3d")

            data = np.zeros((len(x), len(y)))

            for xi, yi in res:
                data[np.where(x == xi)[0][0], np.where(y == yi)[0][0]] += 1 / len(res)

            rows, columns = data.shape

            xpos = np.arange(0, rows, 1)
            ypos = np.arange(0, columns, 1)

            xpos, ypos = np.meshgrid(xpos, ypos)
            xpos, ypos = xpos.flatten(), ypos.flatten()

            dx = dy = np.ones(rows * columns) * 0.5

            ax.bar3d(xpos, ypos, np.zeros(columns * rows), dx, dy, data.flatten())

            x_labels, y_labels = np.meshgrid(x, y)

            ax.w_xaxis.set_ticks(xpos + dx / 2)
            ax.w_xaxis.set_ticklabels(x_labels.flatten())

            ax.w_yaxis.set_ticks(ypos + dy / 2)
            ax.w_yaxis.set_ticklabels(y_labels.flatten())

            ax.set_xlabel('x')
            ax.set_ylabel('y')

            ax.set_zlabel('Frequency')

            plt.show()

        my_hist(res_x, fig, axes[0], k=n)
        my_hist(res_y, fig, axes[1], k=m, color="orange")
        plt.show()
        my_hist_3d(res, x, y)

        # стьюдент
        alpha=0.05
        n = len(res_x)
        diff = (real["mx"] - th["mx"]) * np.sqrt(n) / np.sqrt(real["dx"])
        critical_level = scipy.stats.t.ppf(alpha, n)
        ss = f" check mx: {diff < abs(critical_level)}"
        print(diff < abs(critical_level))
        messagebox.showinfo('hypotesis', ss)

        n = len(res_y)
        diff = (real["my"] - th["my"]) * np.sqrt(n) / np.sqrt(real["dy"])
        critical_level = scipy.stats.t.ppf(alpha, n)
        ss = f" check my: {diff < abs(critical_level)}"
        print(diff < abs(critical_level))
        messagebox.showinfo('hypotesis', ss)

        # хи квадрат
        n = len(res_x)

        chi2 = (n - 1) * real["dx"] / th["dx"]

        chi2_l = scipy.stats.chi2.ppf(alpha / 2, n - 1)
        chi2_r = scipy.stats.chi2.ppf(1 - 0.05 / 2, n - 1)

        print(chi2_l < chi2 < chi2_r)
        ss = f" check dx: {chi2_l < chi2 < chi2_r}"
        print(diff < abs(critical_level))
        messagebox.showinfo('hypotesis', ss)

        n = len(res_y)

        chi2 = (n - 1) * real["dy"] / th["dy"]

        chi2_l = scipy.stats.chi2.ppf(alpha / 2, n - 1)
        chi2_r = scipy.stats.chi2.ppf(1 - alpha / 2, n - 1)

        print(chi2_l < chi2 < chi2_r)
        ss = f" check dy: {chi2_l < chi2 < chi2_r}"
        print(diff < abs(critical_level))
        messagebox.showinfo('hypotesis', ss)


if __name__ == '__main__':
    window = Tk()
    window.geometry('500x450')
    window.configure(bg='#ffe1ca')
    window.title("Ммод 3 лр")
    lbl = Label(window, text=f"((11 - 1) % 9 + 1) = {((11 - 1) % 9 + 1)}", font=("Arial Bold", 15), fg='#1e90ff')
    lbl.grid(column=1, row=0)

    entry = Entry(window)
    entry.grid(column=0, row=2)

    btn = Button(window,text="Click", command=task2)
    btn.grid(column=0, row=5)

    label = Label(window)
    label.grid(column=0, row=7)

    window.mainloop()
