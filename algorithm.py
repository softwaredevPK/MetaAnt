
class Vehicle():
    route = []


class Ant():

    def __init__(self, weight_limit):
        self.route = []
        self.weight_limit = weight_limit
        self.current_weight = 0

    def increase_weight(self, weight):
        self.current_weight += weight
