import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FormatStrFormatter






class Graph:
    def __init__(self, name, p_xlabel, p_ylabel):
        self.name = name
        self.values = [] # stored values depending on the type of graph eg distances
        self.x = []
        self.y = []
        self.height = 5
        self.width = 8
        self.count = 0
        self.bg_color = "white"
        self.line_color = "blue"
        self.xlabel_txt = p_xlabel
        self.ylabel_txt = p_ylabel
        self.xlabel = ''
        self.ylabel = ''
        self.lables = [self.xlabel, self.ylabel]

        self.graph = plt.figure()
        self.ax = self.graph.add_subplot(1, 1, 1)
        plt.title('Sentiment analysis')











        # Setting the background color of the plot
        # using set_facecolor() method


        plt.figure(figsize=(7, 5))


    def plot(self):
        matplotlib.rc('xtick', color=self.line_color)
        matplotlib.rc('ytick', color=self.line_color)



        self.x.append(self.count)
        self.y.append(self.values[self.count])
        self.count += 1

        plt.cla()



        self.xlabel = plt.xlabel(self.xlabel_txt)
        self.ylabel = plt.ylabel(self.ylabel_txt)
        self.xlabel.set_color(self.line_color)
        self.ylabel.set_color(self.line_color)




        plt.plot(self.x, self.y, color=self.line_color)
        self.ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))


        plt.savefig(f'{self.name}.png', facecolor=self.bg_color, transparent=True, dpi=70)

    def clear_graph(self):
        self.x = []
        self.y = []
        self.count = 0
        self.values = [] # clears data for the graph

# distance_graph = plt.figure()
# distance_graph.add_subplot(1, 1, 1)
# plt.figure(figsize=(8, 5))
#
# x = []
# count = 0
# y = []
# distances = []
#
#
#
# def clear_plot():
#     plt.clf()
#     plt.cla()
#     print('asdadsdadsadasdasdsa')
#
#
# def distance_func(count):
#     # xcoords = []
#     with open("distances.txt", 'r') as file:
#         lines = file.readline()
#         distances = [float(i) for i in lines.split()]
#         # if len(distances) > 10:
#         #     for i in range((len(distances)) // 2):
#         #         del distances[i]
#
#         x.append(count)
#         y.append(distances[count])
#         count += 1
#
#     print(len(distances))
#     plt.cla()
#     plt.plot(x, y)
#     plt.savefig("distance_graph.png", dpi=50)
#     return count
#
#
# def animate():
#     ani = animation.FuncAnimation(plt.gcf(), distance_func, interval=500)
#     plt.show()
#
#
# if __name__ == '__main__':
#     animate()

