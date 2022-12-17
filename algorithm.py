import pandas as pd
import numpy as np
from Haversine import haversine
import random


class Vehicle():

    def __init__(self, weight_limit, start_city_index):
        self.route = [start_city_index]
        self.weight_limit = weight_limit
        self.current_weight = 0

    # done
    def increase_weight(self, weight):
        self.current_weight += weight

    # done
    def get_route_distance(self, distance_matrix):
        from_city = self.route[0]
        distance = 0
        for to_city in self.route[1:]:
            distance += distance_matrix[to_city][from_city]
            from_city = to_city
        return distance


class Car(Vehicle):
    ...


class Ant(Vehicle):
    ...


class AntAlgorithm:

    def __init__(self, pheromone_weight=1, visibility_weight=2, start_city_index=0, evaporation_coefficient=0.5):
        self.distance_matrix = None
        self.alfa = pheromone_weight
        self.beta = visibility_weight
        self.start_city_index = start_city_index
        self.evaporation = evaporation_coefficient

    # done
    def read_csv(self, filepath):
        """Expects a csv file with 4 columns: city, lon, lat, demand without headers"""
        return pd.read_csv(filepath, names=["lon", "lat", "demand"])

    # done
    def calculate_distance_matrix(self, cities_data):
        distance_matrix = []
        for city, data in cities_data.iterrows():
            city_array = []
            for second_city, second_data in cities_data.iterrows():
                distance = haversine(data["lon"], data["lat"], second_data["lon"], second_data["lat"])
                city_array.append(distance)
            distance_matrix.append(city_array)
        return pd.DataFrame(distance_matrix)

    # done
    def get_initial_visibility(self):
        """
        Initial visibility as 1/distance beetwen cities
        As you can't divide per 0, we recieve inf number which we replace with 0
        """
        return (1 / self.distance_matrix).replace(np.inf, 0)

    # done
    def get_initial_pheromones(self):
        """
        Return matrix of ones
        """
        matrix_size = len(self.distance_matrix)
        return pd.DataFrame(np.ones([matrix_size, matrix_size]))

    # done
    def update_visibility(self, visibility_matrix, ant):
        last_city = ant.route[-1]
        visibility_matrix[last_city] = 0
        return visibility_matrix

    # done
    def calculate_possibility_of_visit(self, pheromone_matrix, probability_matrix):
        matrix_size = len(self.distance_matrix)
        visit_matrix = pheromone_matrix ** self.alfa * probability_matrix ** self.beta
        possibilities = visit_matrix / (pd.DataFrame(np.ones([matrix_size, matrix_size])) * visit_matrix.sum(1)).transpose()
        return possibilities.cumsum(1)  # cumulative

    # done
    def update_pheromone_matrix(self, ants, pheromones_matrix):
        evaporation_matrix = pheromones_matrix - self.evaporation
        for ant in ants:
            from_city = ant.route[0]
            for to_city in ant.route[1:]:
                evaporation_matrix[to_city][from_city] += 1 / ant.get_route_distance(self.distance_matrix)
                from_city = to_city
        return evaporation_matrix

    def calculate(self, cars, cycles_no, ants_no, csv_file):
        cities_data = self.read_csv(csv_file)
        self.distance_matrix = self.calculate_distance_matrix(cities_data)

        # todo tymczasowe na czas testów
        self.distance_matrix = pd.DataFrame(
            [[0, 10, 12, 11, 14], [10, 0, 13, 15, 8], [12, 13, 0, 9, 14], [11, 15, 9, 0, 16], [14, 8, 14, 16, 0]])

        # todo brakuje handlingu zapotrzebowania i pojemności - przydałby się słownik {"miasto": "zapotrzebowanie"}
        used_routes = []
        for car_number, car in enumerate(cars):
            best_route = None
            for cycle in range(cycles_no):
                best_cycle_route = None
                ants = [Ant(50, self.start_city_index) for i in range(ants_no)] # todo 50 to pojemność

                # preparation
                if cycle == 0:
                    pheromones_matrix = self.get_initial_pheromones()
                for ant in ants:
                    # Step 1
                    visibility_matrix = self.get_initial_visibility()
                    if car_number != 0:
                        ...
                        # todo chyba tutaj trzeba updejtować raz jeszcze visibility o 0 dla miast które były już odwiedzone, dzięki temu ich nie wybierze(przez used_routes)
                    while True:
                        if len(ant.route) == len(self.distance_matrix):
                            break
                        visibility_matrix = self.update_visibility(visibility_matrix, ant)

                        # Step 2
                        cumulitive_possibility_matrix = self.calculate_possibility_of_visit(pheromones_matrix, visibility_matrix)

                        #step 3
                        random_value = random.random()
                        cumulitive_values_from_current_city = cumulitive_possibility_matrix.iloc[ant.route[-1]]
                        new_city_to_go = cumulitive_values_from_current_city[cumulitive_values_from_current_city > random_value].index[0]
                        ant.route.append(new_city_to_go)
                # step 4
                # update pheromone level for next cycle
                pheromones_matrix = self.update_pheromone_matrix(ants, pheromones_matrix)

            # end of cycles
            car.route = best_cycle_route  # todo jeszcze nie wiem jak się wybiera ostateczną i najlepsza trase, na koniec cykli? w trakcie cykli? do rozkminy




# todo aktualnie nie mamy powrotu do bazy(miasta 0), jeśli mmay dodać to wystarczy na końcu poza while do routa poprzez append startowa jak sie nie myle

algorithm = AntAlgorithm()
algorithm.calculate(["car"], 5, 5, "TestData.csv")