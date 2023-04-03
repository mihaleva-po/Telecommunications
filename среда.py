
import numpy as np
from scipy.linalg import solve
from scipy.stats import poisson, binom
import math
import matplotlib.pyplot as plt


# Значения лямбды
lmd = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]

# Генерирование матрицы переходных состояний

n = 100  # Количество слотов
M = [0 for i in range(len(lmd))] # Среднее количество АБ

# Заполнение матрицы
for l in range(len(lmd)): # Смена значений лямбды
    # Создание матрицы n на n
    P = [[] for i in range(n)]
    for i in range(n):
        for j in range(n):
            x = 0  # Количество переданных сообщений (может быть 1 или 0)
            Pr0 = 0  # Произведение верояностей при x = 0
            y = i - j + x  # Подсчет сколько пользователей должно прийти
            if y >= 0:
                if j == 0:
                    # Вероятность, что ни одно сообщение не отправлено
                    R = 1 - binom.pmf(k=1, n=j, p=1)
                else:
                    R = 1 - binom.pmf(k=1, n=j, p=1 / j)
                try:
                    # Вероятность, что придет i абонентов
                    p = lmd[l] ** y / math.factorial(y) * pow(math.e,
                                                           -lmd[l])
                    Pr0 = p * R
                except OverflowError:
                    p = 0
                    Pr0 = p * R

            x = 1  # Количество переданных сообщений равно 1
            Pr1 = 0
            y = i - j + x
            if y >= 0:
                if j == 0:
                    R = binom.pmf(k=1, n=j, p=1)
                else:
                    R = binom.pmf(k=1, n=j, p=1 / j)
                try:
                    p = lmd[l] ** y / math.factorial(y) * pow(math.e,
                                                           -lmd[l])
                    Pr1 = p * R
                except OverflowError:
                    p = 0
                    Pr1 = p * R

            Pr = Pr0 + Pr1
            P[i].append(Pr)
    P = np.array(P)
    print("PP", P.reshape(n, n), '\n')

    # Коээфициенты перед П
    Matrix = [[] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if (i == j):
                Matrix[i].append(P[i][j] - 1)
            else:
                Matrix[i].append(P[i][j])

    Matrix = np.array(Matrix)
    # print("Matrix", Matrix)

    # Замена последнего уравнения условием нормировки
    for i in range(n):
        for j in range(n):
            if i == n - 1:
                Matrix[i][j] = 1
    # print("Matrix", Matrix)

    # Вектор правой части уравнения
    vector = [0 for i in range(n - 1)]
    vector.append(1)

    # Решение СЛАУ и получение стационарного распределения
    x = solve(Matrix, vector)
    # print("П = ", x)

    S = []  # Хранит индекс состояний
    for i in range(n):
        S.append(i)

    # Среднее количество абонентов, находящихся
    # в системе множественного доступа
    for i in range(n):
        M[l] += S[i] * x[i]
    print("Среднее количество абонентов в системе равно ", M[l])


#  По лр1

# Количество абонентов по распределению Пуассона
P_l = []
for i in range(len(lmd)):
    P_l.append(np.random.poisson(lmd[i],n))

# Начальное количество абонентов в каждом слоте для всех лямбд
N_start = [[0 for i in range(n)] for j in range(len(lmd))]

# Конечное количество абонентов в каждом слоте для всех лямбд
N_finish = [[0 for i in range(n)] for j in range(len(lmd))]

for j in range(len(lmd)): # Лямбда
    for i in range(n): # Номер слота
        R = 0 # Количество абонентов, передающих сообщение
        if N_start[j][i] != 0:
            R = np.random.binomial(N_start[j][i],
                                   1 / N_start[j][i], 1)
        I = 0  # Индикаторная функция
        if R == 1:
            I = 1
        N_finish[j][i] = N_start[j][i] + P_l[j][i] - I
        if i < n - 1:
            N_start[j][i + 1] = N_finish[j][i]

# Сумма пользователей во всех слотах
sum_N = [0 for i in range(len(lmd))]
for i in range(len(lmd)): # Смена лямбды
    for j in range(n): # Номер слота
        sum_N[i] += N_finish[i][j]

# Среднее количество абонентов
N_mean = [0 for i in range(len(lmd))]
for i in range(len(lmd)):
    N_mean[i] = (1/n) * sum_N[i]



# Построение графиков
fig, ax = plt.subplots()

ax.plot(lmd, M, marker='o', label = 'С помощью решений систем уравнений')
ax.plot(lmd, N_mean, marker='o', label = 'Через количество АБ в слоте k')

# Добавление сетки
ax.grid(alpha=0.6)

# Подписи осей
plt.ylabel("Среднее количество абонентов в системе")
plt.xlabel("Интенсивность входного потока")
ax.set_title("График зависимости")
plt.legend(loc = 0)
# Ограничение графика
ax.set_ylim(0, 20)
# Ограничение графика
# ax.set_ylim(0, 20)

plt.show()


