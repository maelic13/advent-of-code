def parse_forest(x_coord: int, y_coord: int, forest: list[list[int]]
                 ) -> tuple[list[int], list[int], list[int], list[int]]:
    horizontal = forest[x_coord]
    vertical = [x[y_coord] for x in forest]

    left = list(reversed(horizontal[:y_coord]))
    right = horizontal[y_coord + 1:]
    upwards = list(reversed(vertical[:x_coord]))
    downwards = vertical[x_coord + 1:]

    return left, right, upwards, downwards


def visible(x_coord: int, y_coord: int, forest: list[list[int]]) -> bool:
    left, right, upwards, downwards = parse_forest(x_coord, y_coord, forest)

    tree_visible = False
    for direction in [left, right, upwards, downwards]:
        if not direction:
            tree_visible = True
            break
        if all(x < forest[x_coord][y_coord] for x in direction):
            tree_visible = True
            break
    return tree_visible


def scenic_score(x_coord: int, y_coord: int, forest: list[list[int]]) -> int:
    left, right, upwards, downwards = parse_forest(x_coord, y_coord, forest)

    score = 1
    for direction in [left, right, upwards, downwards]:
        i = 0
        for i, tree_height in enumerate(direction):
            if tree_height >= forest[x_coord][y_coord]:
                break
        score *= i + 1
    return score


def advent8() -> None:
    with open("inputs/day8.txt", "r") as file:
        lines = file.readlines()

    forest: list[list[int]] = []
    for line in lines:
        forest.append([int(char) for char in line.strip()])

    # part 1
    counter = 0
    for x_coord, tree_line in enumerate(forest):
        for y_coord, _ in enumerate(tree_line):
            if visible(x_coord, y_coord, forest):
                counter += 1
    print(counter)

    # part 2
    scenic_scores: list[int] = []
    for x_coord, tree_line in enumerate(forest):
        for y_coord, _ in enumerate(tree_line):
            scenic_scores.append(scenic_score(x_coord, y_coord, forest))
    print(max(scenic_scores))


if __name__ == "__main__":
    advent8()
