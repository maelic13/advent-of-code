import numpy as np


class Valve:
    def __init__(self, name: str, index: int, flow_rate: int) -> None:
        self.name = name
        self.index = index
        self.flow_rate = flow_rate
        self.connections: list[Valve] = []
        self.is_open = False

    def __repr__(self) -> str:
        return f"Valve({self.name}, flow rate: {self.flow_rate})"

    def add_connections(self, valves: list["Valve"]) -> None:
        self.connections += valves

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False


class ValveSystem:
    def __init__(self, valves: list[Valve]) -> None:
        self.valves = valves
        self.adjacency = self.calculate_adjacency_matrix(valves)
        self.valve_distances = self.apd(self.adjacency)

    @staticmethod
    def calculate_adjacency_matrix(valves: list[Valve]) -> np.matrix:
        adjacency_matrix = np.matrix(np.zeros((len(valves), len(valves))))
        for valve in sorted(valves, key=lambda v: v.index):
            for connection in valve.connections:
                adjacency_matrix[valve.index, connection.index] = 1
        return adjacency_matrix

    def apd(self, adjacency_matrix: np.matrix) -> np.matrix:
        dimension = adjacency_matrix.shape[0]
        if all(adjacency_matrix[i, j] for i in range(dimension)
               for j in range(dimension) if i != j):
            return adjacency_matrix

        z_matrix = adjacency_matrix ** 2
        b_matrix = np.matrix([
            [1 if i != j and (adjacency_matrix[i, j] == 1 or z_matrix[i, j] > 0)
             else 0 for j in range(dimension)]
            for i in range(dimension)])

        t_matrix = self.apd(b_matrix)
        x_matrix = t_matrix * adjacency_matrix
        degree = [sum(adjacency_matrix[i, j] for j in range(dimension)) for i in range(dimension)]

        d_matrix = np.matrix([
            [2 * t_matrix[i, j] if x_matrix[i, j] >= t_matrix[i, j] * degree[j]
             else 2 * t_matrix[i, j] - 1 for j in range(dimension)]
            for i in range(dimension)])

        return d_matrix

    def find_by_name(self, name: str) -> Valve:
        for valve in self.valves:
            if valve.name == name:
                return valve
        raise RuntimeError(f"No valve with name {name} found.")

    def find_by_index(self, index: int) -> Valve:
        for valve in self.valves:
            if valve.index == index:
                return valve
        raise RuntimeError(f"No valve with index {index} found.")

    def search(self, valve: Valve, score, time: int
               ) -> tuple[int, list[Valve]]:
        if time <= 0:
            return score

        if valve.flow_rate > 0:
            valve.open()
            time -= 1
            score += time * valve.flow_rate

        best_score = score
        for target_valve in [v for v in self.valves if not v.is_open and v.flow_rate > 0]:
            temp_score = self.search(
                target_valve, score, time - self.valve_distances[valve.index, target_valve.index])
            if temp_score > best_score:
                best_score = temp_score
        valve.close()
        return best_score


def advent16() -> None:
    with open("inputs/day16.txt", "r") as file:
        lines = file.readlines()

    valves: list[Valve] = []
    valves_connections: list[list[str]] = []
    for index, line in enumerate(lines):
        name = line.strip().split()[1]
        flow_rate = line.strip().split()[4]
        flow_rate = flow_rate.replace(";", "")
        flow_rate = flow_rate.replace("rate=", "")
        connections = line.strip().split("; ")[1].split()[4:]
        valves_connections.append([c.replace(",", "") for c in connections])
        valves.append(Valve(name, index, int(flow_rate)))

    for valve, connections in zip(valves, valves_connections):
        valve.add_connections([v for v in valves if v.name in connections])
    valve_system = ValveSystem(valves)
    valve_system.find_by_name("AA").open()

    # part 1
    time = 30
    pressure_released = valve_system.search(valve_system.find_by_name("AA"), 0, time)
    print(pressure_released)


if __name__ == "__main__":
    advent16()
