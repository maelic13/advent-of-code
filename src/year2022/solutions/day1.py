if __name__ == "__main__":
    with open("../inputs/day1.txt", "r") as file:
        lines = file.readlines()

    elves_calories: list[list[int]] = [[]]
    for line in lines:
        if line == "\n":
            elves_calories.append([])
            continue
        elves_calories[-1].append(int(line))

    # part 1
    print(max(sum(x) for x in elves_calories))

    # part 2
    print(sum(sorted(sum(x) for x in elves_calories)[-3:]))
