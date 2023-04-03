
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal

M = 0.5 # Мат ожидание
sigma = 0.8 # Сигма
N = 1000 # Количество элементов

X = normal(M, sigma, N)
k = 30 # окошко диапазона

klv_windows = N - k
Y = [0 for i in range(len(X))]
for i in range(klv_windows):
    for j in range(k):
        if (j + i) < len(X):
            Y[i] += X[j + i]

for i in range(len(Y)):
    Y[i] = Y[i] / k

nomer_N = []  # Хранит индекс состояний
for i in range(N):
    nomer_N.append(i)

# Вычисление сигмы
print("Сигма X", np.std(X))
print("Сигма Y", np.std(Y))
print("Мат ожидание X", np.mean(X))
print("Мат ожидание Y", np.mean(Y))

# Построение графиков
fig, ax = plt.subplots()

ax.plot(nomer_N, X, marker='o',
            label='Массив X')
ax.plot(nomer_N, Y, marker='o',
            label='Массив Y')

# Добавление сетки
ax.grid(alpha=0.6)

# Подписи осей
plt.ylabel(" ")
ax.set_title("")
plt.xlabel("Номер элемента")
plt.legend(loc=0)

plt.show()


















