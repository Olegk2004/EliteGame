import matplotlib.pyplot as plt


def create_plot(galaxy):
    plt.figure(figsize=(20, 10))
    plt.gca().set_facecolor('black')

    # Отрисовка графика систем
    for system in galaxy.systems:
        plt.scatter(system.x, system.y, color='white', s=3)  # Точка для каждой системы
        plt.text(system.x, system.y, system.name, color='white', fontsize=6, ha='center', va='bottom')

    x = []
    y = []
    for m in galaxy.matches:
        x.append(m.x)
        y.append(m.y)
        for i in galaxy.matches[m]:
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
