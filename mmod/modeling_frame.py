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


class ModelingFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.ind = 0
        m, lambd, mu = self.master.parse_data()
        T0 = 0
        application_n = 0
        T_end_processing = [None] * application_n
        t_n = config.t_n
        n = config.n
        delta = t_n / n
        T_now = T0

        T_processing = []
        state = []
        que = []
        declined = []
        processed = []
        in_process = None

        T = []
        last = T0
        application_id = 0
        is_processing = False
        max_time = 0

        while max_time < t_n:
            r = random.random()
            tau = -(1 / lambd) * math.log(r)
            last += tau
            T.append(last)
            max_time = last
            application_n += 1

        for i in range(application_n):
            r = random.random()
            t_ser = -(1 / mu) * math.log(r)
            T_processing.append(t_ser)

        print('Generated T:', T)
        T_end_processing = [None] * application_n

        while T_now <= t_n:
            # сначала проверим , что мы не закончили когонибудь обрабатывать
            if is_processing:
                if T_now > T_end_processing[in_process]:
                    processed.append(in_process)
                    is_processing = False
                    in_process = None

            # событие произошло
            while T_now >= T[application_id]:
                # занят
                if is_processing:
                    if len(que) < m:
                        que.append(application_id)
                    else:
                        declined.append(application_id)
                else:
                    if len(que) == 0:
                        in_process = application_id
                    else:
                        in_process = que[0]
                        que.pop(0)
                    is_processing = True
                    T_end_processing[in_process] = T_processing[in_process] + T_now

                application_id += 1

            res = {
                "T_now": T_now,
                "in_process": in_process,
                "end_time": T_end_processing,
                "processed": processed,
                "declined": declined,
                "всего в сиситеме": int(in_process is not None) + len(que),
                "que": que,
            }
            state.append(res)
            print("\n\n", res, "\n\n")
            self.label_pair('state', res)
            T_now += delta

    def label_pair(self, title, value):
        lbl = Label(self, text=title)
        lbl.grid(column=0, row=self.ind)
        lbl = Label(self, text=value)
        lbl.grid(column=1, row=self.ind)
        self.ind += 1
