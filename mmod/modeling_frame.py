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
        self.list_box = Listbox(self, width=230, height=50)
        # self.columnconfigure(0, minsize=2000)
        # self.rowconfigure(0, minsize=1000)
        self.list_box.grid()
        self.ind = 0
        m, lambd, mu = self.master.parse_data()
        T0 = 0
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
        application_n = 0

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
        print(f'{T_processing=}')
        T_finish_processing = []

        app_num = 0
        for t, t_proc in zip(T, T_processing):
            self.labels_row(
                'app num:',
                app_num,
                'время прихода',
                f'{t:.2f}',
                'время обработки',
                f'{t_proc:.2f}',
            )
            app_num += 1

        self.labels_row('')

        while T_now <= t_n:
            # сначала проверим , что мы не закончили когонибудь обрабатывать
            if is_processing:
                if T_finish_processing and T_now > T_finish_processing[-1]:
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
                    T_finish_processing.append(T_processing[in_process] + T_now)

                application_id += 1

            res = {
                "T_now": T_now,
                "in_process": in_process,
                "finish_proc_time": T_finish_processing,
                "processed": processed,
                "declined": declined,
                "всего в системе": int(in_process is not None) + len(que),
                "queue": que,
            }
            state.append(res)

            self.labels_row(*[f'{k}: {w}' for k, w in res.items()])
            T_now += delta

    def labels_row(self, *args):
        res_text = ''
        for i, arg in enumerate(args):
            res_text += str(arg) + '  '
            # lbl = Label(self, text=arg)
            # lbl.grid(column=i, row=self.ind)
        self.list_box.insert(END, res_text)

        # self.ind += 1
