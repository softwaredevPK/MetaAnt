import pandas as pd
import numpy as np
from Haversine import haversine
import random
import warnings
from draw_image import GraphDrawer
warnings.filterwarnings("ignore")


class Vehicle():

    def __init__(self, weight_limit):
        self.route = []
        self.weight_limit = weight_limit
        self.current_weight = 0
        self.distance = 0

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

    # done
    def get_remaining_weight_limit(self):
        return self.weight_limit - self.current_weight


class Car(Vehicle):
    pass


class Ant(Vehicle):
    pass


class AntAlgorithm:

    def __init__(self, pheromone_weight=1, visibility_weight=2, start_city_index=0, evaporation_coefficient=0.5):
        if not 0 <= evaporation_coefficient <= 1:
            raise KeyError("evaporation_coefficient should be from [0,1]")
        self.distance_matrix = None
        self.demand_array = None
        self.alfa = pheromone_weight
        self.beta = visibility_weight
        self.start_city_index = start_city_index
        self.evaporation = evaporation_coefficient
        self.cities_data = None

    # done
    def read_csv(self, filepath):
        """Expects a csv file with 4 columns: city, lon, lat, demand without headers"""
        return pd.read_csv(filepath, names=["city", "lon", "lat", "demand"])

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
    def get_demand_array(self, cities_data):
        demand = []
        for city, data in cities_data.iterrows():
            demand.append(data["demand"])
        return pd.array(demand)

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
        possibilities = (visit_matrix / (pd.DataFrame(np.ones([matrix_size, matrix_size])) * visit_matrix.sum(1)).transpose()).replace(np.NaN, 0)
        return possibilities.cumsum(1)  # cumulative

    # done
    def update_pheromone_matrix(self, ants, pheromones_matrix):
        evaporation_matrix = (1 - self.evaporation) * pheromones_matrix
        for ant in ants:
            from_city = ant.route[0]
            for to_city in ant.route[1:]:
                evaporation_matrix[to_city][from_city] += 1 / ant.get_route_distance(self.distance_matrix)
                from_city = to_city
        return evaporation_matrix

    # done
    def update_visibility_by_demand(self, visibility_matrix, weight_limit):
        cities_to_skip = visibility_matrix[self.demand_array > weight_limit].index
        for city in cities_to_skip:
            visibility_matrix[city] = 0
        return visibility_matrix

    # done
    def get_best_ant_route(self, ants):
        best_ant = None
        best_distance = None
        for ant in ants:
            distance = ant.get_route_distance(self.distance_matrix)
            if best_ant is None or distance < best_distance:
                best_distance = distance
                best_ant = ant
        return best_ant, best_distance

    # done
    def update_initial_visibility_matrix_by_used_routes(self, visibility_matrix, routes):
        for route in routes:
            for visited_city in route[1:]:
                visibility_matrix[visited_city] = 0
        return visibility_matrix

    # done
    def calculate(self, cars, cycles_no, ants_no, csv_file):
        self.cities_data = self.read_csv(csv_file)
        self.distance_matrix = self.calculate_distance_matrix(self.cities_data)
        self.demand_array = self.get_demand_array(self.cities_data)
        used_routes = []

        for car_number, car in enumerate(cars):
            best_distance = None
            best_ant = None
            if car_number == 0:
                initial_visibility_matrix = self.get_initial_visibility()

            for cycle in range(cycles_no):
                ants = [Ant(car.weight_limit) for i in range(ants_no)]

                # preparation
                if cycle == 0:
                    pheromones_matrix = self.get_initial_pheromones()
                for ant in ants:

                    ant.route.append(self.start_city_index)
                    # Step 1
                    visibility_matrix = initial_visibility_matrix.copy()

                    while True:
                        visibility_matrix = self.update_visibility(visibility_matrix, ant)
                        visibility_matrix = self.update_visibility_by_demand(visibility_matrix, ant.get_remaining_weight_limit())

                        if (visibility_matrix == 0).all().all():
                            # there is nowhere to go
                            break

                        # Step 2
                        cumulitive_possibility_matrix = self.calculate_possibility_of_visit(pheromones_matrix, visibility_matrix)

                        #step 3
                        random_value = random.random()
                        cumulitive_values_from_current_city = cumulitive_possibility_matrix.iloc[ant.route[-1]]
                        new_city_to_go = cumulitive_values_from_current_city[cumulitive_values_from_current_city > random_value].index[0]

                        ant.route.append(new_city_to_go)
                        ant.increase_weight(self.demand_array[new_city_to_go])

                    # Each ant is supposed to return to start point
                    ant.route.append(self.start_city_index)

                # step 4
                # update pheromone level for next cycle
                pheromones_matrix = self.update_pheromone_matrix(ants, pheromones_matrix)

                # best route from cycle
                best_cycle_ant, best_cycle_distance = self.get_best_ant_route(ants)
                if best_ant is None or best_cycle_distance < best_distance:
                    best_distance = best_cycle_distance
                    best_ant = best_cycle_ant

            # end of all cycles

            # save best route from experiment to car
            car.route = best_ant.route
            car.current_weight = best_ant.current_weight
            car.distance = best_distance
            used_routes.append(best_ant.route)

            # next car is not supposed to go to the same cities
            initial_visibility_matrix = self.update_initial_visibility_matrix_by_used_routes(initial_visibility_matrix,
                                                                                             used_routes)

        return cars, sum([i.distance for i in cars])

    def draw_image(self, paths):
        cities_data = self.cities_data
        GraphDrawer(paths, cities_data=cities_data).run()


"""
W celu lepszego pokazania rysowania, zedytowoaliśmy TestData by się współrzędne nie nakłądały na siebie
Czyli odległości - punkty na mapie są fałszywe dla tego zbioru!
"""



print('TestData:')
to_draw_algorithm = AntAlgorithm()
to_draw_solved_cars, distance = to_draw_algorithm.calculate([Vehicle(1000) for i in range(0, 3)], 5, 8, "TestData.csv")
print("Sum of distance:", distance)
for car in to_draw_solved_cars:
    print(car.route, car.current_weight, car.distance)


print('TestData: start city 2')
# works with different city to start, with more cars than required
algorithm = AntAlgorithm(start_city_index=2)
solved_cars, distance = algorithm.calculate([Vehicle(1000) for i in range(0, 5)], 5, 8, "TestData.csv")
print("Sum of distance:", distance)
for car in solved_cars:
    print(car.route, car.current_weight, car.distance)

print('TownsData, 5 cycles, 8 ants')
# works with different city to start, with more cars than required
algorithm = AntAlgorithm()
solved_cars, distance = algorithm.calculate([Vehicle(1000) for i in range(0, 5)], 5, 8, "TownsData.csv")
print("Sum of distance:", distance)
for car in solved_cars:
    print(car.route, car.current_weight, car.distance)


print('TownsData, 5cycles,  30 ants')
# works with different city to start, with more cars than required
algorithm = AntAlgorithm()
solved_cars, distance = algorithm.calculate([Vehicle(1000) for i in range(0, 5)], 5, 8, "TownsData.csv")
print("Sum of distance:", distance)
for car in solved_cars:
    print(car.route, car.current_weight, car.distance)


print('TownsData, 10cycles, 20 ants')
# works with different city to start, with more cars than required
algorithm = AntAlgorithm()
solved_cars, distance = algorithm.calculate([Vehicle(1000) for i in range(0, 5)], 10, 20, "TownsData.csv")
print("Sum of distance:", distance)
for car in solved_cars:
    print(car.route, car.current_weight, car.distance)



# drawing first test data
to_draw_algorithm.draw_image([i.route for i in to_draw_solved_cars])