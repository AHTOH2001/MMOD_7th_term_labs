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
import json
from collections import Counter
from math import pi
import matplotlib
import scipy
from scipy import integrate
import scipy.optimize as opt

T0 = 0
# T_n = 1000
# 100
# n = 10000
# 1000000
application_n = 0


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
storage = {}
import math
def cout_charachteristics(lambd, mu,m):
    file = f"resMmod{m}.json"
    my_file = open(file, "w+")
    s = ""
    to_file = {}
    P = []
    ro=lambd/mu
    print("ro",ro)
    print(m)
    P.append((1-ro)/(1-math.pow(ro,m+2)))
    for i in range(1,m+2):
        P.append(round(math.pow(ro,i)*P[0],5))
    s += f"Вероятности состояний {P} \n\n"
    print("Вероятности состояний",P)
    to_file["Вероятности состояний"] = P
    P_decline = P[-1]
    s += f"Вероятность отказа {P_decline} \n\n"
    print("Вероятность отказа", P_decline)
    to_file["Вероятность отказа"] = P_decline
    q = 1-P[-1]
    A = lambd*q
    s += f"Относительная пропускная способность { q} \n\n"
    print("Относительная пропускная способность", q)
    to_file["Относительная пропускная способность"] = q
    s+= f"Абсолютная пропускная способность {A} \n\n"
    print("Абсолютная пропускная способность", A)
    to_file["Абсолютная пропускная способность"] = A
    r = math.pow(ro,2)*(1-math.pow(ro,m)*(m+1-m*ro))/((1-math.pow(ro,m+2))*(1-ro))
    s += f"Среднее число заявок в очереди, ожидающих обслуживания  {r} \n\n"
    print("Среднее число заявок в очереди, ожидающих обслуживания", r)
    to_file["Среднее число заявок в очереди, ожидающих обслуживания"] = r
    omega = ro*q
    s+= f"среднее число заявок, находящееся под обслуживанием {round(omega,3)} \n\n"
    print("среднее число заявок, находящееся под обслуживанием",round(omega,3))
    to_file["среднее число заявок, находящееся под обслуживанием"] = round(omega,3)
    k = omega+r
    s += f"среднее число заявок в системе {round(k,3)} \n\n"
    print("среднее число заявок в системе",round(k,3))
    to_file["среднее число заявок в системе"] = round(k,3)
    t_wait = r/lambd
    s += f"Среднее время ожидания заявок в очереди {round(t_wait, 3)}(ч) \n\n"
    print("Среднее время ожидания заявок в очереди (ч)", round(t_wait, 3))
    to_file["Среднее время ожидания заявок в очереди (ч)"] = round(t_wait, 3)
    t_total = t_wait+q/mu
    s+= f"Среднее время пребывания заявки в смо {round(t_total, 3)} (ч) \n\n"
    print("Среднее время пребывания заявки в смо (ч)", round(t_total, 3))
    to_file["Среднее время пребывания заявки в смо (ч)"] = round(t_total, 3)
    messagebox.showinfo('Характеристики', "\n\n" +s+"\n\n")
    to_file["!!!!MmM!!!"]=m
    # my_file.write("m=3")
    json.dump(to_file, my_file)
    my_file.close()

def model(T_n,in_process,is_processing,T_now, delta, T_end_processing, processed, application_id, T, que,  declined, T_processing, state, lambd,
          mu ,m):
    statistics = []

    while T_now < T_n:
        # print("HERE",T_now + delta , T_n,)
        # сначала проверим , что мы не закончили когонибудь обрабатывать
        if is_processing:
            if T_now > T_end_processing[in_process]:
                processed.append(in_process)
                is_processing = False
                in_process = None
        # else:
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

            # if not is_changed and application_id == 0:
            #             #     statistics["00"] += T[0]
            #             #     is_changed = True
            #             #     last_time_checked = T[0]
            application_id += 1
            # statistics.append(int(in_process is not None) + len(que))
        # if in_process is None:
        # TODO:HERE


        res = {"T_now": T_now, "in_process": in_process, "end_time": T_end_processing, "processed": processed,
               "declined": declined, "всего в сиситеме": int(in_process is not None) + len(que), "que": que}
        state.append(res)
        s_res = f"""T_now : {T_now}, in_process : {in_process} ,  processed : {processed},
               "declined": {declined}, "всего в сиситеме": {int(in_process is not None) + len(que)}, "que": {que}"""
        print("\n\n", res, "\n\n")
        # messagebox.showinfo('Состояние сиситемы', "\n\n"+s_res+"\n\n")
        statistics.append(int(in_process is not None) + len(que))
        T_now += delta
    # print("HEREEEEEEE",statistics)
    P_pract = []
    for i in range(m+1):
        p_p = statistics.count(i)/(len(statistics)*1.0)
        P_pract.append(p_p)



    print(state[-1])
    # print(statistics)
    # print("HEREERERERe", P_pract)
    cout_charachteristics(lambd=lambd, mu = mu, m = m)

def clicked(i):
    # m=3

    s = ""
    res = []
    for j in range(i):
        data = storage[j].get()
        if isfloat(data) or data.isdigit():
            data = eval(data)
            res.append(data)


    T_n, n  = res[0],res[1]

    T0 = 0
    lambd = 4
    mu = 0.52
    application_n = 0

    delta = T_n / n
    T_now = T0

    state = []
    # время обслуживания  i-ой заявки
    T_processing = []
    que = []
    declined = []
    processed = []
    in_process = None

    # время прихода хаявок
    T = []
    last = T0
    application_id = 0
    is_processing = False
    max_time = 0


    while max_time < T_n:
        r = random.random()
        tau = -(1 / lambd) * math.log(r)
        # tau = np.random.exponential(1 / lambd)
        last += tau
        T.append(last)
        max_time = last
        application_n += 1

    print("APPLICATION N", application_n)
    last_time_checked = None
    # время обслуживания
    for i in range(application_n):
        r = random.random()
        t_ser = -(1 / mu) * math.log(r)
        # t_ser = np.random.exponential(mu)
        T_processing.append(t_ser)
    print("T = ", T)
    print("T_processing = ", T_processing)
    T_end_processing = [None] * application_n
    print("T_end_processing", T_end_processing)
    print("delta = ", delta)
    messagebox.showinfo('Исходные данные', "\n\n" + f"T = {T}" +"\n\n" + f"T_end_processing = {T_end_processing}" +  "\n\n"+f"delta = {delta}")
    is_changed = False
    # m = res[2]
    # for i  in [3,4]:
    for i in [3,4]:

        model(T_n,in_process,is_processing,T_now, delta, T_end_processing, processed, application_id, T, que,  declined, T_processing, state, lambd,
          mu ,m=i)

if __name__ == '__main__':
    window = Tk()
    window.geometry('700x450')
    window.configure(bg='#ffe1ca')
    window.title("Ммод 4 лр")
    lbl = Label(window, text=f"Variant  = {11}", font=("Arial Bold", 15), fg='#1e90ff')
    lbl.grid(column=0, row=0)

    lbl = Label(window, text="Введите T_n (длина интрвала от нуля)", font=("Arial Bold", 10), fg='#1e90ff')
    # storage[0] = lbl
    lbl.grid(column=0, row=3)
    txt = Entry(window, width=20, borderwidth=0)
    storage[0] = txt
    txt.grid(column=0, row=5)

    lbl = Label(window, text="Введите n (количество интервалов)", font=("Arial Bold", 10), fg='#1e90ff')
    # storage[1] = lbl
    lbl.grid(column=2, row=3)
    txt = Entry(window, width=20, borderwidth=0)
    storage[1] = txt
    txt.grid(column=2, row=5)

    btn = Button(window, text="Вперед!", bg="blue", fg="black", command=partial(clicked, i=2), borderwidth=0)
    btn.grid(column=6, row=7)
    window.mainloop()
