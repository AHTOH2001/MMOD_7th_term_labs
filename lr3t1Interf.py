import math
import random
from functools import partial
from math import pi
from tkinter import *
from tkinter import messagebox
import scipy.stats as sta
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from collections import Counter
from math import pi
import matplotlib
import scipy
from scipy import integrate
import scipy.optimize as opt

a, b = 0, pi / 2


def my_hist(res, ff, fig, ax, color=None):
    bins = (int)(math.log10(100000) * 2)
    ls = np.linspace(np.min(res), np.max(res), 100)

    ax.cla()
    ax.hist(res, bins=bins, density=True, histtype='step', label='Empirical', color=color)
    ax.plot(ls, [ff(i) for i in ls], color='red')


def my_hist_y(res_x, res_y, ff, fig, ax, color=None):
    bins = (int)(math.log10(100000) * 2)
    ls = np.linspace(np.min(res_y), np.max(res_y), 100)

    ax.cla()
    ax.hist(res_y, bins=bins, density=True, histtype='step', label='Empirical', color=color)
    xx = sum(res_x) / len(res_x)
    res = []
    for i in ls:
        res.append(ff(xx, i))
    ax.plot(ls, res, color='red')
    # МЕТОД НЕЙМАНА


def get_xyz(fx, fy_x, fy, W=math.sqrt(2) / 2, a=0, b=pi / 2, n=1000000):
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


def dens():
    ANSWER = {}
    x, y = sp.symbols('x y')
    expn = "0.5*sin(x+y)"

    gfg = sp.sympify(expn)
    print(gfg)
    f = sp.lambdify(sp.symbols('x, y'), expn)
    a, b = 0, pi / 2
    fy = sp.integrate(expn, (x, a, b))
    fx = sp.integrate(expn, (y, a, b))
    print('f(x):', fx)
    print('f(y):', fy)
    dep = sp.simplify(sp.Mul(fx, fy))
    print(dep)
    ind_flag = dep.equals(expn)
    print(dep.equals(expn))
    # if dep.equals(expn):

    # не независимы
    # условные вероятности
    fx_y = sp.simplify(gfg / fy)
    fy_x = sp.simplify(gfg / fx)
    print('f(x|y)', fx_y)
    print('f(y|x)', fy_x)
    ANSWER['f(x)'] = fx
    ANSWER['f(y)'] = fy
    ANSWER['f(x|y)'] = fx_y
    ANSWER['f(y|x)'] = fy_x
    fx = sp.lambdify(sp.symbols('x'), fx)
    fy = sp.lambdify(sp.symbols('y'), fy)
    fy_x = sp.lambdify(sp.symbols('x,y'), fy_x)
    def fy_x_max(x):
        return 1 / (math.sin(x) + math.cos(x))

    res_x_big, res_y_big = get_xyz(fx=fx, fy_x=fy_x_max, fy=fy_x, n=1000000)

    ANSWER['fx'] = fx
    ANSWER['fy'] = fy
    ANSWER['fy_x'] = fy_x
    ANSWER['f'] = f
    ANSWER['res_x_big'] = res_x_big
    ANSWER['res_y_big'] = res_y_big
    ANSWER["is_independant"] = ind_flag

    return ANSWER


def graf(f, fx, fy_x,res_x_big,res_y_big):
    def fy_x_max(x):
        return 1 / (math.sin(x) + math.cos(x))

    # res_x_big, res_y_big = get_xyz(fx=fx, fy_x=fy_x_max, fy=fy_x, n=100000)

    fig, axes = plt.subplots(2, 1)

    my_hist(res_x_big, fx, fig, axes[0])
    my_hist_y(res_x_big, res_y_big, fy_x, fig, axes[1], color="orange")
    plt.show()

    res_x, res_y = get_xyz(fx=fx, fy_x=fy_x_max, fy=fy_x, n=10000)

    np.random.seed(19680801)

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

    ax.plot_surface(ls1, ls2, np.array([f(*point) for point in zip(ls1, ls2)]), color="orange")
    plt.show()


def dens_info(ANSWER):
    messagebox.showinfo('Вероятности',
                        f"f(x): {ANSWER['f(x)']} \n f(y): {ANSWER['f(y)']} \n f(x|y): {ANSWER['f(x|y)']} \n f(y|x): {ANSWER['f(y|x)']}")
    if ANSWER["is_independant"]:
        messagebox.showinfo('Вероятности',
                            "Независмы")
    else:
        messagebox.showinfo('Вероятности',
                            "Зависмы")


def calc_teor(res_x, res_y,f,alpha=0.05):

    x, y = sp.symbols('x y')
    # xf(x)
    expn = "0.5*x*(sin(x)+cos(x))"
    a, b = 0, pi / 2
    m_x_t = sp.integrate(expn, (x, a, b))
    print(m_x_t)
    expn = "0.5*y*(sin(y)+cos(y))"
    m_y_t = sp.integrate(expn, (y, a, b))
    print(m_y_t)

    expn = "0.5*x*x*(sin(x)+cos(x))"
    d_x_t = sp.integrate(expn, (x, a, b)) - m_x_t ** 2
    print(d_x_t)
    expn = "0.5*y*y*(sin(y)+cos(y))"
    d_y_t = sp.integrate(expn, (y, a, b)) - m_y_t ** 2
    print(d_y_t)
    expn = f"(x-{m_x_t})*(y-{m_y_t})*0.5*sin(x+y)"
    cov = sp.integrate(expn, (x, a, b), (y, a, b))
    r_t = cov / (math.sqrt(d_x_t * d_y_t))
    print(r_t)
    s = f"M : {[m_x_t, m_y_t]}," + "\n\n" + f" D: {[d_x_t, d_y_t]}," +"\n\n"+f"r: {[r_t]}"+"\n\n"
    # messagebox.showinfo('theoritic',s)

    m_x = sum(res_x) / len(res_x)
    m_y = sum(res_y) / len(res_y)

    tmp_x = (np.array(res_x) - m_x)
    tmp_y = (np.array(res_y) - m_y)

    d_x = (tmp_x @ tmp_x) / (len(res_x) - 1)
    d_y = (tmp_y @ tmp_y) / (len(res_y) - 1)

    r = (tmp_x @ tmp_y) / (len(res_x) * np.sqrt(d_x * d_y))

    gamma = 1.0 - alpha
    delta_x = d_x * sta.t.ppf(gamma, len(res_x) - 1) / np.sqrt(len(res_x) - 1)
    delta_y = d_y * sta.t.ppf(gamma, len(res_y) - 1) / np.sqrt(len(res_y) - 1)

    lx = ((len(res_x) - 1) * d_x) / scipy.stats.chi2.ppf(1 - alpha / 2, len(res_x) - 1)
    rx = ((len(res_x) - 1) * d_x) / scipy.stats.chi2.ppf(alpha / 2, len(res_x) - 1)

    ly = ((len(res_y) - 1) * d_y) / scipy.stats.chi2.ppf(1 - alpha / 2, len(res_y) - 1)
    ry = ((len(res_y) - 1) * d_y) / scipy.stats.chi2.ppf(alpha / 2, len(res_y) - 1)

    r_scaled = np.arctanh(r)
    r_scaled_std = 1 / np.sqrt(len(res_x) - 3)
    z = scipy.stats.norm.ppf(1 - alpha / 2)
    rxy_l, rxy_r = np.tanh(r_scaled - z * r_scaled_std), np.tanh(r_scaled + z * r_scaled_std)

    # s = f"M : {[m_x, m_y]}," + "\n\n" + f" D: {[d_x, d_y]}," + "\n\n" + f"r: {[r]}" + "\n\n"
    s+= f"m_x_interval: {(round(m_x - delta_x, 5), round(m_x + delta_x, 5))}," +"\n\n"
    s+= f"m_y interval: {(round(m_y - delta_y, 5), round(m_y + delta_y, 5))}," +"\n\n"
    s+= f"d_x interval: {(round(lx, 5), round(rx, 5))}," +"\n\n"
    s+= f"d_y interval: { (round(ly, 5), round(ry, 5))}," +"\n\n"
    s+= f"r interval: { (round(rxy_l, 5), round(rxy_r, 5))}," +"\n\n"
    messagebox.showinfo('both', s)

    # стьюдент
    n = len(res_x)
    diff = (m_x - m_x_t) * np.sqrt(n) / np.sqrt(d_x)
    critical_level = scipy.stats.t.ppf(alpha, n)
    ss = f" check mx: {diff < abs(critical_level)}"
    print(diff < abs(critical_level))
    messagebox.showinfo('hypotesis', ss)

    n = len(res_y)
    diff = (m_y - m_y_t) * np.sqrt(n) / np.sqrt(d_y)
    critical_level = scipy.stats.t.ppf(alpha, n)
    ss = f" check my: {diff < abs(critical_level)}"
    print(diff < abs(critical_level))
    messagebox.showinfo('hypotesis', ss)

    #хи квадрат
    n = len(res_x)

    chi2 = (n - 1) * d_x / d_x_t

    chi2_l = scipy.stats.chi2.ppf(alpha / 2, n - 1)
    chi2_r = scipy.stats.chi2.ppf(1 - 0.05 / 2, n - 1)

    print(chi2_l < chi2 < chi2_r)
    ss = f" check dx: {chi2_l < chi2 < chi2_r}"
    print(diff < abs(critical_level))
    messagebox.showinfo('hypotesis', ss)

    n = len(res_y)

    chi2 = (n - 1) * d_y / d_y_t

    chi2_l = scipy.stats.chi2.ppf(alpha / 2, n - 1)
    chi2_r = scipy.stats.chi2.ppf(1 - 0.05 / 2, n - 1)

    print(chi2_l < chi2 < chi2_r)
    ss = f" check dy: {chi2_l < chi2 < chi2_r}"
    print(diff < abs(critical_level))
    messagebox.showinfo('hypotesis', ss)
    # http://statistica.ru/theory/znachimost-koeffitsienta-korrelyatsii-doveritelnyy-interval/
    # z = (np.arctanh(r) - np.arctanh(r_t)) * np.sqrt(len(res_x) - 3)
    # critical = scipy.stats.norm.ppf(0.05)
    # print(z < abs(critical))
    # ss = f" check r: {z < abs(critical)}"
    # print(diff < abs(critical_level))
    # messagebox.showinfo('hypotesis', ss)
# http://old.gsu.by/biglib/GSU/%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9/%D0%AD%D0%9A%D0%B8%D0%A2%D0%92/%D1%80%D1%83%D0%BA-%D0%BB%D0%B0%D0%B1-%D0%9C%D0%A1/3%20%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B8%20%D0%BD%D0%B5%D0%B8%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D0%BE%D0%B2.pdf

def get_real(res_x, res_y, alpha=0.05):
    m_x = sum(res_x) / len(res_x)
    m_y = sum(res_y) / len(res_y)

    tmp_x = (np.array(res_x) - m_x)
    tmp_y = (np.array(res_y) - m_y)

    d_x = (tmp_x @ tmp_x) / (len(res_x) - 1)
    d_y = (tmp_y @ tmp_y) / (len(res_y) - 1)

    r = (tmp_x @ tmp_y) / (len(res_x) * np.sqrt(d_x * d_y))

    gamma = 1.0 - alpha
    delta_x = d_x * sta.t.ppf(gamma, len(res_x) - 1) / np.sqrt(len(res_x) - 1)
    delta_y = d_y * sta.t.ppf(gamma, len(res_y) - 1) / np.sqrt(len(res_y) - 1)

    lx = ((len(res_x) - 1) * d_x) / scipy.stats.chi2.ppf(1 - alpha / 2, len(res_x) - 1)
    rx = ((len(res_x) - 1) * d_x) / scipy.stats.chi2.ppf(alpha / 2, len(res_x) - 1)

    ly = ((len(res_y) - 1) * d_y) / scipy.stats.chi2.ppf(1 - alpha / 2, len(res_y) - 1)
    ry = ((len(res_y) - 1) * d_y) / scipy.stats.chi2.ppf(alpha / 2, len(res_y) - 1)

    r_scaled = np.arctanh(r)
    r_scaled_std = 1 / np.sqrt(len(res_x) - 3)
    z = scipy.stats.norm.ppf(1 - alpha / 2)
    rxy_l, rxy_r = np.tanh(r_scaled - z * r_scaled_std), np.tanh(r_scaled + z * r_scaled_std)

    s = f"M : {[m_x, m_y]}," + "\n\n" + f" D: {[d_x, d_y]}," + "\n\n" + f"r: {[r]}" + "\n\n"
    s+= f"m_x_interval: {(round(m_x - delta_x, 5), round(m_x + delta_x, 5))}," +"\n\n"
    s+= f"m_y interval: {(round(m_y - delta_y, 5), round(m_y + delta_y, 5))}," +"\n\n"
    s+= f"d_x interval: {(round(lx, 5), round(rx, 5))}," +"\n\n"
    s+= f"d_y interval: { (round(ly, 5), round(ry, 5))}," +"\n\n"
    # s+= f"r interval: { (round(rxy_l, 5), round(rxy_r, 5))}," +"\n\n"
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



if __name__ == '__main__':
    ANSWER = dens()
    window = Tk()
    window.geometry('500x450')
    window.configure(bg='#ffe1ca')
    window.title("Ммод 3 лр")
    lbl = Label(window, text=f"((11 - 1) % 9 + 1) = {((11 - 1) % 9 + 1)}", font=("Arial Bold", 15), fg='#1e90ff')
    lbl.grid(column=1, row=0)
    lbl = Label(window, text="0.5*sin(x+y)", font=("Arial Bold", 25), fg='#1e90ff')
    lbl.grid(column=1, row=0)
    lbl = Label(window, text=f"a = {a}", font=("Arial Bold", 15), fg='#1e90ff')
    lbl.grid(column=0, row=1)
    lbl = Label(window, text=f"b = {b}", font=("Arial Bold", 15), fg='#1e90ff')
    lbl.grid(column=2, row=1)

    btn = Button(window, text="рассчитать плотности!", bg="blue", fg="black", command=partial(dens_info, ANSWER=ANSWER))
    btn.grid(column=0, row=5)
    btn = Button(window, text="графики гистограммы", bg="blue", fg="black",
                 command=partial(graf, f=ANSWER["f"], fx=ANSWER["fx"], fy_x=ANSWER["fy_x"],res_y_big=ANSWER["res_y_big"],res_x_big=ANSWER["res_x_big"]))
    btn.grid(column=2, row=5)

    btn = Button(window, text="Рассчитать реальные", bg="blue", fg="black",
                 command=partial(get_real, res_y=ANSWER["res_y_big"],res_x=ANSWER["res_x_big"]))
    btn.grid(column=0, row=7)
    btn = Button(window, text="Рассчитать теоритические", bg="blue", fg="black",
                 command=partial(calc_teor, f=ANSWER["f"], res_y=ANSWER["res_y_big"],res_x=ANSWER["res_x_big"]))
    btn.grid(column=2, row=7)
    window.mainloop()
