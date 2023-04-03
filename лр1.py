import numpy as np
import matplotlib.pyplot as plt

k = 1000 # Количество слотов

# Значения лямбды
l = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]

# Количество абонентов по распределению Пуассона
P_l = []
for i in range(len(l)):
    P_l.append(np.random.poisson(l[i],k))

# Начальное количество абонентов в каждом слоте для всех лямбд
N_start = [[0 for i in range(k)] for j in range(len(l))]

# Конечное количество абонентов в каждом слоте для всех лямбд
N_finish = [[0 for i in range(k)] for j in range(len(l))]

for j in range(len(l)): # Лямбда
    for i in range(k): # Номер слота
        R = 0 # Количество абонентов, передающих сообщение
        if N_start[j][i] != 0:
            R = np.random.binomial(N_start[j][i],
                                   1 / N_start[j][i], 1)
        I = 0  # Индикаторная функция
        if R == 1:
            I = 1
        N_finish[j][i] = N_start[j][i] + P_l[j][i] - I
        if i < k - 1:
            N_start[j][i + 1] = N_finish[j][i]

# Сумма пользователей во всех слотах
sum_N = [0 for i in range(len(l))]
for i in range(len(l)): # Смена лямбды
    for j in range(k): # Номер слота
        sum_N[i] += N_finish[i][j]

# Среднее количество абонентов
N_mean = [0 for i in range(len(l))]
for i in range(len(l)):
    N_mean[i] = (1/k) * sum_N[i]

fig, ax = plt.subplots()

x = l # Значения лямбды
y = N_mean # Значения среднего количества абонентов

ax.plot(x, y, marker='o')

# Добавление сетки
ax.grid(alpha=0.6)

# Подписи осей
plt.ylabel("Среднее количество абонентов в системе")
plt.xlabel("Интенсивность входного потока")
ax.set_title("График зависимости при #i слотах" # k)
# Ограничение графика
ax.set_ylim(0, 20)

# # Среднее количество слотов
# T_mean = [0 for i in range(len(l))]
# for i in range(len(l)):
#     T_mean[i] = N_mean[i] / l[i]
#
# fig, ax = plt.subplots()
#
# # x = l # Значения лямбды
# # y = T_mean # Значения среднего количества абонентов
# #
# # ax.plot(x, y, marker='o')
#
# # Добавление сетки
# ax.grid(alpha=0.6)
#
# # Подписи осей
# plt.xlabel("Интенсивность входного потока")
# plt.ylabel("Среднее количество слотов необходимое для передачи сообщения")
# ax.set_title("График зависимости")

# Ограничения графика
ax.set_ylim(0, 20)

plt.show()























