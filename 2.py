from control.matlab import *
import matplotlib.pyplot as plt
def zveno(p):
    #переходная ф-я
    y,x = step(p)
    plt.plot(x,y,"b")
    plt.title('Переходная хар-ка')
    plt.ylabel('Aмплитуда')
    plt.xlabel('Время')
    plt.grid(True)
    plt.show()
    #импульсная ф-я
    y,x = impulse(p)
    plt.plot(x,y,"b")
    plt.title('Импульсная хар-ка')
    plt.ylabel('Aмплитуда')
    plt.xlabel('Время')
    plt.grid(True)
    plt.show()
    #ЛАЧХ ЛФЧХ
    mag, phase, omega = bode(p, dB=True)
    plt.plot()
    plt.show()
# передаточная ф-я, задаем с клавиатуры числитель и знаменатель и тип звена в родительном падеже
tip = ('безынерционного звена')
p = tf([1], [10e-10,1])
zveno(p)