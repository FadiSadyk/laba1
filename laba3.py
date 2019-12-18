from math import sqrt
from control.matlab import *
from control import *
from numpy import *

k = 1
Tp = 3
Td = 3

num_gen = [1.]
den_gen = [6.0, 1.]
num_hydro = [0.01 * 2.0, 1]
den_hydro = [0.05 * 6.0, 1]
num_iu = [20]
den_iu = [5.0, 1]
num_p = [0, k]
den_p = [0, 1]
num_i = [0, 1]
den_i = [Tp, 0]
num_d = [Td, 0]
den_d = [0, 1]

W_p = tf(num_p, den_p)
W_i = tf(num_i, den_i)
W_d = tf(num_d, den_d)
W_r = W_p + W_i + W_d

W_gen = tf(num_gen, den_gen)
W_iu = tf(num_iu, den_iu)
W_hydro = tf(num_hydro, den_hydro)
# замкнутая САУ
W_z = feedback(W_iu * W_hydro * W_gen * W_r, 1)
# разомкнутая САУ
W_r = W_iu * W_hydro * W_gen * W_r


def check_criteria(z):
    A, t = step(z)
    A_max = max(A)
    if A[-2] - 0.01 * A[-1] < A[-1] < A[-2] + 0.01 * A[-1]:
        const_value = A[-1]
    else:
        print("Система неустойчива")
    for i in range(1, len(t)):
        if const_value * 0.95 > A[-i] or A[-i] > const_value * 1.05:
            T = t[-i]
            break
    real, image, freq = nyquist_plot(z)
    amp = []
    for i in range(len(real)):
        amp.append(sqrt(real[i] ** 2 + image[i] ** 2))
    M = max(amp) / amp[0]
    o_r = (A_max - const_value) * 100 / const_value
    print("Время регулирования:", T, '\n' "Требуемое: 10")
    print("Показатель колебательности:", M, '\n' "Требуемое: 1.15")
    print("Перерегулирование:", o_r, "%", '\n' "Требуемое: 20 %")


def direct(z):
    A, t = step(z)
    A_max = max(A)
    amp = []
    if A[-2] - 0.01 * A[-1] < A[-1] < A[-2] + 0.01 * A[-1]:
        const_value = A[-1]
    else:
        print("Система неустойчива")
    for i in range(1, len(A)):
        if A[i] > A[i + 1] and A[i] > A[i - 1]:
            amp.append(A[i])
        if const_value * 0.95 > A[-i] or A[-i] > const_value * 1.05:
            T = t[-i]
            break
    for i in range(len(A)):
        if amp[0] == A[i]:
            t_max = t[i]
    o_r = (A_max - const_value) * 100 / const_value
    n_koleb = len(amp)
    psi = 1 - amp[1] / amp[0]
    print("Прямые оценки качества переходного процесса:")
    print("Время регулирования:", T)
    print("Перерегулирование:", o_r, "%")
    print("Колебательность системы:", n_koleb)
    print("Степень затухания:", psi)
    print("Величина достижения первого максимума:", amp[0])
    print("Время достижения первого максимума:", t_max)


def indirect(z):
    polus = pole(z)
    a = []
    b = []
    m = []
    for i in range(len(polus)):
        a.append(-polus[i].real)
        b.append(polus[i].imag)
        m.append(abs(b[i] / a[i]))
    a_min = abs(min(a))
    T = 3 / a_min
    n_koleb = max(m)
    o_r = e ** (pi / n_koleb)
    psi = 1 - e ** (-2 * pi / n_koleb)
    print("По распределению корней на комплексной плоскости замкнутой САУ:")
    print("Время регулирования:", T)
    print("Перерегулирование:", o_r)
    print("Колебательность системы:", n_koleb)
    print("Степень затухания:", psi)


def ach(z):
    real, image, freq = nyquist_plot(z)
    amp = []
    fi = None
    magn = None
    for i in range(len(real)):
        amp.append(sqrt(real[i] ** 2 + image[i] ** 2))
    M = max(amp) / amp[0]
    for i in range(len(amp)):
        if 0.9 * amp[0] < amp[i] < amp[0] * 1.1:
            w_sr = freq[i]
    T = 3 * pi / w_sr
    magnitude, phase, freq = bode(z, Plot=True)
    for i in range(len(freq)):
        if -0.01 < magnitude[i] < 0.01:
            fi = phase[i]
        if -1.2 * pi < magnitude[i] < -0.8 * pi:
            magn = magnitude[i]
    if fi is None:
        fi = "не найден"
    if magn is None:
        magn = "не найден"
    print("По логарифмическим частотным характеристикам:")
    print("Показатель колебательности:", M)
    print("Время регулирования:", T)
    print("Запас по амплитуде:", magn)
    print("Запас по фазе:", fi)


def kio(z):
    A, t = step(z)
    if A[-2] - 0.01 * A[-1] < A[-1] < A[-2] + 0.01 * A[-1]:
        const_value = A[-1]
    else:
        print("Система неустойчива")
    sum = ((A[0] - const_value) ** 2) * t[0]
    for i in range(1, len(A)):
        sum += ((A[i] - const_value) ** 2) * (t[i] - t[i - 1])
    print("Квадратичная интегральная оценка качества:", sum)


# y, x = step(W_z)
# plt.plot(x, y, "b")
# plt.title('Переходная хар-ка')
# plt.ylabel('Aмплитуда')
# plt.xlabel('Время')
# plt.grid(True)
# plt.show()
# check_criteria(W_z)
# direct(W_z)
# indirect(W_z)
# ach(W_z)
# kio(W_z)


# magnitude, phase, freq = bode(W_z, Plot=True)
# plt.figure()
# plt.plot(freq, phase)
# plt.grid(True)
# plt.title("ФЧХ")
# plt.show()

# pzmap(W_z)
# plt.grid(True)
# plt.show()
