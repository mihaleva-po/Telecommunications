
import numpy as np
from scipy.linalg import solve
from scipy.stats import poisson, binom
import math


# Генерирование матрицы переходных состояний

n = 4  # Количество состояний
k = 4  # Количество слотов
# k = n
lmd = 0.4  # Значение лямбды

# 1 пункт


# Создание матрицы n на n
P = [[] for i in range(n)]
# Заполнение матрицы
for i in range(n):
    for j in range(n):
        # print("j, i", j, i)
        x = 0 # Количество переданных сообщений (может быть 1 или 0)
        Pr0 = 0 # Произведение верояностей при x = 0
        y = i - j + x # Подсчет сколько пользователей должно прийти
        if y >= 0:
            if j == 0:
                # Вероятность, что ни одно сообщение не отправлено
                R = 1 - binom.pmf(k=1, n=j, p=1)
            else:
                R = 1 - binom.pmf(k=1, n=j, p=1 / j)
            try:
                # Вероятность, что придет i абонентов
                p = lmd ** y / math.factorial(y) * pow(math.e, -lmd)
                Pr0 = p * R
            except OverflowError:
                p = 0
                Pr0 = p * R

        x = 1 # Количество переданных сообщений равно 1
        Pr1 = 0
        y = i - j + x
        if y >= 0:
            if j == 0:
                R = binom.pmf(k=1, n=j, p=1)
            else:
                R = binom.pmf(k=1, n=j, p=1 / j)
            try:
                p = lmd ** y / math.factorial(y) * pow(math.e, -lmd)
                Pr1 = p * R
            except OverflowError:
                p = 0
                Pr1 = p * R

        Pr = Pr0 + Pr1
        P[i].append(Pr)


P = np.array(P)
print(P.reshape(n, n), '\n')

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
vector = [0 for i in range(n-1)]
vector.append(1)


# Решение СЛАУ и получение стационарного распределения
x = solve(Matrix, vector)
print("П = ", x)



# 2 пункт


S = [] # Хранит номера состояний
for i in range(n):
    S.append(i)

# Среднее количество абонентов, находящихся
# в системе множественного доступа
M = np.dot(x, S)
print("Среднее количество абонентов в системе равно ", M)




