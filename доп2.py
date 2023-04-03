

import numpy as np
import matplotlib.pyplot as plt


# Количество слотов
k = 1000

# Лямбда
lmd = 0.2


# Количество абонентов, у которых появляются сообщения для передачи
P_lmd = np.random.poisson(lmd,k)
# print("P_lmd")
# print(max(P_lmd))
# print(min(P_lmd))

# i - номер слота
# Начальное и конечное количество абонентов
N_start = []
N_finish = []

for i in range(k):
    N_start.append(0)
    N_finish.append(0)


max_R = 0
for i in range(k): # Номер слота
    R = 0 # Количество абонентов, передающих сообщение
    if N_start[i] != 0:
        R = np.random.binomial(N_start[i], 0.4, 1)

    I = 0  # Индикаторная функция
    if R == 1:
        I = 1
    N_finish[i] = N_start[i] + P_lmd[i] - I

    if i < k - 1:
        N_start[i + 1] = N_finish[i]
    if max_R < R:
        max_R = R
    # print(R)

# print(max_R)
# print("N_st")
# print(min(N_start))
# print(max(N_start))
# print("N_f")
# print(max(N_finish))
# print(min(N_finish))

# Строим график зависимости количества абонентов в слоте от
# номера слота

x = [] # Номер слота
for i in range(k):
    x.append(i)
y = N_finish # Количество абонентов


fig, ax = plt.subplots()
ax.plot(x, y, marker='o')

# Добавление сетки
ax.grid(alpha=0.6)

# Подписи осей
plt.xlabel("Номер слота")
plt.ylabel("Количество абонентов")
ax.set_title("График зависимости")
# ax.set_ylim(0, 20)


plt.show()























