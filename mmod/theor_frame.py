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


class TheorFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # self.columnconfigure(0, minsize=2000)
        # self.rowconfigure(0, minsize=1000)
        self.ind = 0
        m, lambd, mu = self.master.parse_data()
        P = []

        ro = lambd / mu
        # self.label_pair('Ro:', ro)

        P.append((1 - ro) / (1 - math.pow(ro, m + 2)))
        for i in range(1, m + 2):
            P.append(math.pow(ro, i) * P[0])

        for ind, p in enumerate(P):
            self.label_pair(f"Вероятность {ind} заявки в системе:", f'{p:.8f}')
        P_decline = P[-1]
        self.label_pair("Вероятность отказа:", f'{P_decline:.3f}')

        q = 1 - P[-1]
        A = lambd * q
        self.label_pair("Относительная пропускная способность:", f'{q:.3f}')
        self.label_pair("Абсолютная пропускная способность:", f'{A:.3f}')

        r = (
            math.pow(ro, 2)
            * (1 - math.pow(ro, m) * (m + 1 - m * ro))
            / ((1 - math.pow(ro, m + 2)) * (1 - ro))
        )

        self.label_pair(
            "Среднее число заявок в очереди, ожидающих обслуживания", f'{r:.3f}'
        )

        omega = ro * q
        self.label_pair(
            "среднее число заявок, находящееся под обслуживанием", f'{omega:.3f}'
        )

        k = omega + r
        self.label_pair("среднее число заявок в системе", f'{k:.3f}')

        t_wait = r / lambd
        self.label_pair("Среднее время ожидания заявок в очереди (ч)", f'{t_wait:.3f}')

        t_total = t_wait + q / mu
        self.label_pair("Среднее время пребывания заявки в смо (ч)", f'{t_total:.3f}')

    def label_pair(self, title, value):
        lbl = Label(self, text=title)
        lbl.grid(column=0, row=self.ind)
        lbl = Label(self, text=value)
        lbl.grid(column=1, row=self.ind)
        self.ind += 1
