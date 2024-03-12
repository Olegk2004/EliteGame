''' Заготовка для игры
import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Super Elite Game")

running = True
while running:

    pygame.display.update()

    for event in pygame.event.get():
        if  event.type == pygame.QUIT:
            running = False
            pygame.quit()
'''
import matplotlib.pyplot as plt
from galaxy import Galaxy

# Создание графика
plt.figure(figsize=(20, 10))
plt.gca().set_facecolor('black')

# Cоздание галактики
new_galaxy = Galaxy(0x5A4A, 0x0248, 0xB753)
new_galaxy.make_systems()
new_galaxy.create_matches()

# Отрисовка графика систем
for system in new_galaxy.systems:
    plt.scatter(system.x, system.y, color='white', s=3)  # Точка для каждой системы
    plt.text(system.x, system.y, system.name, color='white', fontsize=6, ha='center', va='bottom')

x = []
y = []
for m in new_galaxy.matches:
    x.append(m.x)
    y.append(m.y)
    for i in new_galaxy.matches[m]:
        x.append(i.x)
        y.append(i.y)
        x.append(m.x)
        y.append(m.y)
    plt.plot(x, y)
    x = []
    y = []

plt.gca().invert_yaxis()
plt.grid(False)
plt.show()
