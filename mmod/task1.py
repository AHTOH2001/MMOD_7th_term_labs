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
from .modeling_frame import ModelingFrame
from .theor_frame import TheorFrame


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

        btn = Button(self, text="Моделирование", command=self.modeling)
        btn.grid(column=0, row=5, columnspan=2)

    def parse_data(self):
        m = int(self.m_entry.get())
        lambd = int(self.lambd_entry.get())
        mu = float(self.mu_entry.get())
        print(f'Entered data: {m=}, {lambd=}, {mu=}')
        return m, lambd, mu

    def calc_teor(self):
        frame = self.master.master.create_new_frame(TheorFrame)
        frame.grid()

    def modeling(self):
        frame = self.master.master.create_new_frame(ModelingFrame)
        frame.grid()
