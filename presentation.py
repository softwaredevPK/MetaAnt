
import algorithm as a

"""
W celu lepszego pokazania rysowania, zedytowoaliśmy TestData by się współrzędne nie nakłądały na siebie
Czyli odległości - punkty na mapie są fałszywe dla tego zbioru!
"""



print('TestData:')
to_draw_algorithm = a.AntAlgorithm()
to_draw_solved_cars, distance = to_draw_algorithm.calculate([a.Vehicle(1000) for i in range(0, 3)], 5, 8, "TestData.csv")
print("Sum of distance:", distance)
for car in to_draw_solved_cars:
    print(car.route, car.current_weight, car.distance)


print('TestData: start city 2')
# works with different city to start, with more cars than required
algorithm = a.AntAlgorithm(start_city_index=2)
solved_cars, distance = algorithm.calculate([a.Vehicle(1000) for i in range(0, 5)], 5, 8, "TestData.csv")
print("Sum of distance:", distance)
for car in solved_cars:
    print(car.route, car.current_weight, car.distance)

print('TownsData, 5 cycles, 8 ants')
# works with different city to start, with more cars than required
algorithm = a.AntAlgorithm()
solved_cars, distance = algorithm.calculate([a.Vehicle(1000) for i in range(0, 5)], 5, 8, "TownsData.csv")
print("Sum of distance:", distance)
for car in solved_cars:
    print(car.route, car.current_weight, car.distance)


print('TownsData, 5 cycles,  30 ants')
# works with different city to start, with more cars than required
algorithm = a.AntAlgorithm()
solved_cars, distance = algorithm.calculate([a.Vehicle(1000) for i in range(0, 5)], 5, 8, "TownsData.csv")
print("Sum of distance:", distance)
for car in solved_cars:
    print(car.route, car.current_weight, car.distance)


print('TownsData, 10 cycles, 20 ants')
# works with different city to start, with more cars than required
algorithm = a.AntAlgorithm()
solved_cars, distance = algorithm.calculate([a.Vehicle(1000) for i in range(0, 5)], 10, 20, "TownsData.csv")
print("Sum of distance:", distance)
for car in solved_cars:
    print(car.route, car.current_weight, car.distance)



# drawing first test data
to_draw_algorithm.draw_image([i.route for i in to_draw_solved_cars])