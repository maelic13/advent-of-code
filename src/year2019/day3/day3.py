from copy import copy
import numpy as np


class Wire:
    def __init__(self, wire, beginning):
        self._wire = wire
        self._beginning = beginning
        self._end = None
        self._wire_locations = self._calculate_wire_locations()

    def _calculate_wire_locations(self):
        if not self._wire:
            raise RuntimeError("No data for wire!")

        current_location = copy(self._beginning)
        locations = []

        for direction in self._wire:
            command = direction[0]
            steps = int(direction[1:])

            if command == "R":
                for i in range(0, steps):
                    locations.append((current_location[0], current_location[1] + (i + 1)))
                current_location[1] += steps
            elif command == "L":
                for i in range(0, steps):
                    locations.append((current_location[0], current_location[1] - (i + 1)))
                current_location[1] -= steps
            elif command == "U":
                for i in range(0, steps):
                    locations.append((current_location[0] + (i + 1), current_location[1]))
                current_location[0] += steps
            elif command == "D":
                for i in range(0, steps):
                    locations.append((current_location[0] - (i + 1), current_location[1]))
                current_location[0] -= steps
            else:
                raise ValueError("Incorrect command!")
        return locations

    def get_number_of_steps(self, intersection):
        return self._wire_locations.index(intersection) + 1

    def get_wire(self):
        return self._wire

    def get_wire_locations(self):
        return self._wire_locations

    def print_wire(self):
        print(self._wire)


class FrontPanel:
    def __init__(self):
        self._wire1 = None
        self._wire2 = None
        self._center_coordinates = [0, 0]
        self._intersections = []
        self._closest_intersection = None
        self._dist_to_closest = None
        self._quickest_intersection = None
        self._fewest_steps = None

    def _load_wires(self, input_file):
        with open(input_file, "r") as file:
            self._wire1 = Wire(file.readline().split(","), self._center_coordinates)
            self._wire2 = Wire(file.readline().split(","), self._center_coordinates)

    def load_manual_wires(self, wire1, wire2):
        self._wire1 = Wire(wire1, self._center_coordinates)
        self._wire2 = Wire(wire2, self._center_coordinates)

    def _calculate_intersections(self):
        locations1 = self._wire1.get_wire_locations()
        locations2 = self._wire2.get_wire_locations()
        intersections = set(locations1) & set(locations2)
        self._intersections = list(intersections)

    def _calculate_closest_intersection(self):
        min_distance = np.Inf
        closest_intersection = None
        for intersection in self._intersections:
            distance = (abs(intersection[0] - self._center_coordinates[0])
                        + abs(intersection[1] - self._center_coordinates[1]))
            if distance < min_distance:
                min_distance = distance
                closest_intersection = intersection
        self._dist_to_closest = min_distance
        self._closest_intersection = closest_intersection

    def _calculate_quickest_intersection(self):
        if not self._intersections:
            self._calculate_intersections()

        fewest_steps = np.Inf
        for intersection in self._intersections:
            steps1 = self._wire1.get_number_of_steps(intersection)
            steps2 = self._wire2.get_number_of_steps(intersection)
            if (steps1 + steps2) < fewest_steps:
                fewest_steps = steps1 + steps2
                self._quickest_intersection = intersection
                self._fewest_steps = fewest_steps

    def get_wires(self):
        return self._wire1, self._wire2

    def get_intersections(self):
        return self._intersections

    def get_closest_intersection(self):
        return self._closest_intersection

    def get_dist_to_closest(self):
        return self._dist_to_closest

    def get_quickest_intersection(self):
        return self._quickest_intersection

    def get_fewest_steps(self):
        return self._fewest_steps

    def print_intersections(self):
        print(self._intersections)

    def print_wires(self):
        self._wire1.print_wire()
        self._wire2.print_wire()


if __name__ == "__main__":
    input_file = "input.txt"
    panel = FrontPanel()

    panel._load_wires(input_file)
    panel._calculate_intersections()
    panel._calculate_closest_intersection()
    panel._calculate_quickest_intersection()

    num_inter = len(panel.get_intersections())
    closest_intersection = panel.get_closest_intersection()
    dist_to_closest = panel.get_dist_to_closest()
    quickest_intersection = panel.get_quickest_intersection()
    fewest_steps = panel.get_fewest_steps()

    print("Intersections found: {}\n"
          "Closest intersection: {}\n"
          "Distance to closest intersection: {}\n"
          "Quickest intersection: {}\n"
          "Fewest steps to intersection: {}\n"
          .format(num_inter, closest_intersection, dist_to_closest, quickest_intersection,
                  fewest_steps))
