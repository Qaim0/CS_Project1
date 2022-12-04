import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
import pandas as pd



distance_graph = plt.figure()
distance_graph.add_subplot(1, 1, 1)
plt.figure(figsize=(8, 5))

x = []
count = 0
y = []



def clear_plot():
    plt.clf()
    plt.cla()
    print('asdadsdadsadasdasdsa')


def distance_func(count):
    # xcoords = []
    with open("distances.txt", 'r') as file:
        lines = file.readline()
        distances = [float(i) for i in lines.split()]
        # if len(distances) > 10:
        #     for i in range((len(distances)) // 2):
        #         del distances[i]

        x.append(count)
        y.append(distances[count])
        count += 1

    print(len(distances))
    plt.cla()
    plt.plot(x, y)
    plt.savefig("distance_graph.png", dpi=50)
    return count


def animate():
    ani = animation.FuncAnimation(plt.gcf(), distance_func, interval=500)
    plt.show()


if __name__ == '__main__':
    animate()
