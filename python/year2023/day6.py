from math import prod
from time import time


class Race:
    def __init__(self, race_time: int, record_distance: int, speed_for_charging: int = 1) -> None:
        self.race_time = race_time  # milliseconds
        self.record_distance = record_distance  # millimeters
        self.speed_for_charging = speed_for_charging  # millimeters per millisecond

    def __repr__(self) -> str:
        return (f"Race(time: {self.race_time}, record: {self.record_distance}, "
                f"speed for charging: {self.speed_for_charging}")

    def distance(self, time_charging: int) -> int:
        return self.speed_for_charging * time_charging * (self.race_time - time_charging)

    def beats_record(self, time_charging: int) -> bool:
        return self.distance(time_charging) > self.record_distance

    def count_winning_charge_times(self) -> int:
        lower_time: int | None = None
        upper_time: int | None = None

        for time_charging in range(1, self.race_time):
            if self.beats_record(time_charging):
                lower_time = time_charging
                break

        if not lower_time:
            return 0

        for time_charging in range(self.race_time, 1, -1):
            if self.beats_record(time_charging):
                upper_time = time_charging
                break

        return upper_time - lower_time + 1


def day6() -> None:
    with open("inputs/2023/day6.txt", "r") as file:
        lines = file.readlines()

    # part 1
    times = [int(t) for t in lines[0].strip().split()[1:]]
    records = [int(r) for r in lines[1].strip().split()[1:]]
    races = [Race(race_time, record) for race_time, record in zip(times, records)]
    print(prod(race.count_winning_charge_times() for race in races))

    # part 2
    race = Race(int("".join(lines[0].strip().split()[1:])),
                int("".join(lines[1].strip().split()[1:])))
    print(race.count_winning_charge_times())


if __name__ == "__main__":
    start = time()
    day6()
    print(f"Execution time: {round((time() - start))} seconds.")
