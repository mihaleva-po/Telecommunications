
import random
import numpy as np
from scipy.linalg import solve
import matplotlib.pyplot as plt


# Генерирование матрицы переходных состояний
n = 4 # Количество состояний
np.random.seed(132 * 10)
P = np.random.uniform(0,1, [4, 4])

# Подсчет суммы вероятностей
for i in range(4):
    Sum = P[i][0] + P[i][1] + P[i][2] + P[i][3]
    # Изменение значений вероятностей
    P[i][0] = P[i][0] / Sum
    P[i][1] = P[i][1] / Sum
    P[i][2] = P[i][2] / Sum
    P[i][3] = P[i][3] / Sum

P = np.array(P)
P.reshape(n, n)
print("Матрица переходных состояний", '\n', P, '\n')

# Умножение вектора П на матрицу переходных состояний
Matrix = [[] for i in range(4)]
for i in range(4):
  for j in range(4):
    if(i==3): # Последняя строчка системы уравнений
      Matrix[i].append(1)
    elif(i==j):
      Matrix[i].append(P[j][i] - 1)
    else:
      Matrix[i].append(P[j][i])

Matrix = np.array(Matrix)
print("Матрица СЛАУ",'\n', Matrix.reshape(n, n), '\n')

# Вектор правой части уравнения
vector = np.array([0, 0, 0, 1])

# Решение СЛАУ
x = solve(Matrix, vector)

# Стационарное распределение
print("П = ", x, '\n')

k_slot = []
for i in range(n):
    k_slot.append(i)

M = np.dot(x, k_slot)
print("M", M)
# Cтационарное распределение при различных значениях
# начального распределения вероятностей и различных значениях t

rasp = [] # Хранит значения стационарных распределений
k = 10 # Количество шагов
for t in range(k):
    P_step = np.linalg.matrix_power(P, t)
    # Создание вектора начальных состояний
    vector_p = np.random.uniform(0, 1, 4)
    Sum = vector_p[0] + vector_p[1] + vector_p[2] + vector_p[3]
    vector_p[0] = vector_p[0] / Sum
    vector_p[1] = vector_p[1] / Sum
    vector_p[2] = vector_p[2] / Sum
    vector_p[3] = vector_p[3] / Sum
    # Умножение вектора p на матрицу переходных состояний
    rasp.append(np.dot(vector_p, P_step))
    # Стационарное распределение
    print("П = ", rasp[t], ' при t равном ', t)
rasp = np.array(rasp)
print('\n')


# Построение графика зависимости значений стационарного распределения
# от номера шага

# Хранят значение стационарного распределения
rasp_0 = []
rasp_1 = []
rasp_2 = []
rasp_3 = []

# Распределение значений по состояниям
for i in range(len(rasp)):
    for j in range(4):
        if j == 0:
            rasp_0.append(rasp[i][j])
        if j == 1:
            rasp_1.append(rasp[i][j])
        if j == 2:
            rasp_2.append(rasp[i][j])
        if j == 3:
            rasp_3.append(rasp[i][j])

# Значения t
t = []
for i in range(k):
    t.append(i)

fig, ax = plt.subplots()
ax.plot(t, rasp_0, label = 'Состояние 0')
ax.plot(t, rasp_1, label = 'Состояние 1')
ax.plot(t, rasp_2, label = 'Состояние 2')
ax.plot(t, rasp_3, label = 'Состояние 3')
ax.set_ylabel("Стационарное распределение")
ax.set_xlabel("Номер шага")
plt.title('График зависимости стационарного распределения'
          ' от номера шага')
plt.grid() # Добавление сетки
plt.legend(loc = 5)
plt.show()


# Метод имитационного моделирования

# u_const - Номер начального состояния
def model(u_const):
    number_hag = []  # Номер шага
    # Количество попаданий в определенную систему
    N_0 = 0
    N_1 = 0
    N_2 = 0
    N_3 = 0
    k = 1000  # Количество переходов
    u = u_const
    # Хранят значения стац распределения
    # по методу имитационного моделирования
    P_0 = [0 for i in range(k)]
    P_1 = [0 for i in range(k)]
    P_2 = [0 for i in range(k)]
    P_3 = [0 for i in range(k)]

    for i in range(k):
        number_hag.append(i + 1)
        r = random.uniform(0, 1)
        # Создание интервалов состояний
        h0 = P[u][0]
        h1 = P[u][0] + P[u][1]
        h2 = h1 + P[u][2]
        h3 = h2 + P[u][3]

        # Определяем к какому интервалу принадлежит r
        if r <= h0:
            N_0 += 1
            u = 0
        elif r <= h1:
            N_1 += 1
            u = 1
        elif r <= h2:
            N_2 += 1
            u = 2
        elif r <= h3:
            N_3 += 1
            u = 3
        P_0[i] = N_0 / (i + 1)
        P_1[i] = N_1 / (i + 1)
        P_2[i] = N_2 / (i + 1)
        P_3[i] = N_3 / (i + 1)

    H_0 = N_0 / k
    H_1 = N_1 / k
    H_2 = N_2 / k
    H_3 = N_3 / k

    print("Значение стационарного распределения "
          "Марковского случайного процесса "
          "при начальном состоянии", u_const )
    print(H_0, '\n', H_1, '\n', H_2, '\n', H_3, '\n')

    # Построение графика
    fig1, ax1 = plt.subplots()
    ax1.plot(number_hag, P_0, label='Состояние 0')
    ax1.plot(number_hag, P_1, label='Состояние 1')
    ax1.plot(number_hag, P_2, label='Состояние 2')
    ax1.plot(number_hag, P_3, label='Состояние 3')
    ax1.set_ylabel("Стационарное распределение")
    ax1.set_xlabel("Номер шага")
    plt.title('При начальном состоянии #i' # u_const)
    plt.grid()
    plt.legend()
    plt.show()


model(0) # При начальном состоянии 0
model(1)
model(2)
model(3)
















