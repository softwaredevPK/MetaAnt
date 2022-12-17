import matplotlib.pyplot as plt


class GraphDrawer:
    def __init__(self, paths: list, cities_data):
        self.paths = paths
        self.figure = plt.figure(figsize=(10, 10))
        self.figure_ax = self.figure.add_subplot(1, 1, 1)
        self.cities_data = cities_data
        self._depot_color = 'k'
        self._customer_color = 'steelblue'
        self.colors = ["red", "orange", "blue", "dark", "purple"]

    def _draw_points(self):
        x = round(self.cities_data.iloc[0]['lon'], 0)
        y = round(self.cities_data.iloc[0]['lat'], 0)
        self.figure_ax.scatter([x], [y], c=self._depot_color, label='depot', s=40)

        remaining_x = [round(self.cities_data.iloc[i]['lon'], 0) for i in self.cities_data.index[1:]]
        remaining_y = [round(self.cities_data.iloc[i]['lat'], 0) for i in self.cities_data.index[1:]]
        self.figure_ax.scatter(remaining_x,
                               remaining_y, c=self._customer_color, label='customer', s=20)
        plt.pause(0.5)

    def run(self):
        self._draw_points()
        self.figure.show()

        for i, path in enumerate(self.paths):
            try:
                color = self.colors[i]
            except KeyError:
                color = self.colors[-1]
            self._draw_line(path, color)
        plt.pause(100)

    def _draw_line(self, path, color="darksalmon"):
        for i in range(1, len(path)):
            x1 = round(self.cities_data.iloc[path[i - 1]]['lon'], 0)
            y1 = round(self.cities_data.iloc[path[i - 1]]['lat'], 0)
            x2 = round(self.cities_data.iloc[path[i]]['lon'], 0)
            y2 = round(self.cities_data.iloc[path[i]]['lat'], 0)
            x_list = [x1, x2]
            y_list = [y1, y2]
            self.figure_ax.plot(x_list, y_list, color=color, linewidth=1.5, label='line')
            plt.pause(0.35)
