def parse_forest(x_coord: int, y_coord: int, forest: list[list[int]]
                 ) -> tuple[list[int], list[int], list[int], list[int]]:
    horizontal = forest[x_coord]
    vertical = [x[y_coord] for x in forest]

    left = horizontal[:y_coord]
    left.reverse()
    right = horizontal[y_coord + 1:]
    upwards = vertical[:x_coord]
    upwards.reverse()
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


if __name__ == "__main__":
    with open("inputs/day8.txt", "r") as FILE:
        LINES = FILE.readlines()

    FOREST: list[list[int]] = []
    for LINE in LINES:
        FOREST.append([int(char) for char in LINE.strip()])

    # part 1
    COUNTER = 0
    for X, TREE_LINE in enumerate(FOREST):
        for Y, _ in enumerate(TREE_LINE):
            if visible(X, Y, FOREST):
                COUNTER += 1
    print(COUNTER)

    # part 2
    SCENIC_SCORES: list[int] = []
    for X, TREE_LINE in enumerate(FOREST):
        for Y, _ in enumerate(TREE_LINE):
            SCENIC_SCORES.append(scenic_score(X, Y, FOREST))
    print(max(SCENIC_SCORES))
