from math import sqrt, atan, degrees
from control.matlab import *
import matplotlib.pyplot as plt
from control import *
from numpy import *

num_oc = [0.1, 0]
den_oc = [3.0, 1.]
num_gen = [1.]
den_gen = [6.0, 1.]
num_hydro = [0.01 * 2.0, 1]
den_hydro = [0.05 * 6.0, 1]
num_iu = [20]
den_iu = [5.0, 1]

W_oc = tf(num_oc, den_oc)
W_gen = tf(num_gen, den_gen)
W_iu = tf(num_iu, den_iu)
W_hydro = tf(num_hydro, den_hydro)
# замкнутая САУ
W_z = feedback(W_iu * W_hydro * W_gen, W_oc)
# разомкнутая САУ
W_r = W_iu * W_hydro * W_gen * W_oc


# переходная характеристика
def perehod(p):
    y, x = step(p)
    plt.plot(x, y, "b")
    plt.title('Переходная хар-ка')
    plt.ylabel('Aмплитуда')
    plt.xlabel('Время')
    plt.grid(True)
    plt.show()


# полюса передаточной ф-и
def pole(p):
    polus = pole(p)
    k = 0
    r = 0
    print('Значения полюсов передаточной ф-и:', polus)
    for i in polus:
        r += 1
        if i <= 0:
            k += 1
    if k == r:
        print('Анализ показывает, что САУ устойчива')
    else:
        print('Анализ показывает, что САУ неустойчива')


# критерий Найквиста на разомкнутой САУ
def nyquist(p):
    real, image, freq = nyquist_plot(p)
    plt.title('Nyquist Diagram ')
    plt.ylabel('Imaginary Axis')
    plt.xlabel('Real Axis')
    nyquist(p)
    plt.grid(True)
    plt.plot()
    plt.show()
    r = -1
    for i in range(len(real)):
        if real[i] < 0 and image[i] < 0.001:
            print("Запас устойчивости по амлитуде:",  1 + real[i])
            break
        if 0.9 < (real[i] ** 2 + image[i] ** 2) < 1.1:
            r = i
    if r != -1:
        print("Запас устойчивости по фазе: ", degrees(atan(image[r]/real[r])))
    else:
        print("Запас устойивости по фазе не определен")

# критерий Михайлова
def mihailov(p):
    den_k = p.den[0]
    k = den_k[0]
    polinom = []
    xw = 0
    yw = 0
    x = []
    y = []
    for w in arange(0, 1.5, 0.01):
        for i in range(len(k)):
            polinom.append(k[i] * ((complex(0, 1)) ** ((len(k) - i) - 1)))
            xw += polinom[i].real * (w ** ((len(k) - i) - 1))
            yw += polinom[i].imag * (w ** ((len(k) - i) - 1))
        x.append(xw)
        y.append(yw)
        xw = 0
        yw = 0
        polinom = []
    plt.figure(1)
    plt.title("Годограф Михайлова")
    plt.plot(x, y)
    plt.ylabel('Im')
    plt.xlabel('Re')
    plt.grid()
    plt.show()
    key = 1
    for i in range(1, len(x)):
        if (x[i] > 0 and (x[i - 1]) < 0) or (x[i] < 0 and (x[i - 1]) > 0) or (y[i] > 0 and (y[i - 1]) < 0) or (y[i] < 0 and (y[i - 1]) > 0):
            key += 1
    if key == len(k) - 1:
        print("Система устойчива по критерию Михайлова")


# ЛФЧХ ЛАЧХ
def ch_h(p):
    bode(p, Plot=True)
    plt.plot
    plt.grid(True)
    plt.show()


# критерий Гурвица
def gurvic(p):
    den_k = p.den[0]
    k = den_k[0]
    matrix = [[0 for i in range(len(k) - 1)] for i in range(len(k) - 1)]
    chet = []
    net = []
    for i in range(len(k)):
        if i % 2 == 0:
            chet.append(k[i])
        else:
            net.append(k[i])
    while len(chet) != len(net):
        if len(chet) > len(net):
            net.append(0)
        else:
            chet.append(0)
    for i in range(len(k) - 1):
        for j in range(len(chet)):
            jm = j + i // 2
            if i % 2 == 0:
                matrix[i][jm] = net[j]
            else:
                matrix[i][jm] = chet[j]
    determinant = linalg.det(matrix)
    print(determinant)

#k_oc = 13.88154997
