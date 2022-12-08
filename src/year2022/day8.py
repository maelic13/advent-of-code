def visible(x_coord: int, y_coord: int, height: int, trees: list[list[int]]) -> bool:
    tree_visible = False
    horizontal = trees[x_coord]
    vertical = [x[y_coord] for x in trees]

    left = horizontal[:y_coord]
    right = horizontal[y_coord + 1:]
    upwards = vertical[:x_coord]
    downwards = vertical[x_coord + 1:]

    for direction in [left, right, upwards, downwards]:
        if not direction:
            tree_visible = True
            break
        if all(x < height for x in direction):
            tree_visible = True
            break
    return tree_visible


def scenic_score(x_coord: int, y_coord: int, height: int, trees: list[list[int]]) -> int:
    horizontal = trees[x_coord]
    vertical = [x[y_coord] for x in trees]

    left = horizontal[:y_coord]
    left.reverse()
    right = horizontal[y_coord + 1:]
    upwards = vertical[:x_coord]
    upwards.reverse()
    downwards = vertical[x_coord + 1:]

    score = 1
    for direction in [left, right, upwards, downwards]:
        i = 0
        for i, tree_height in enumerate(direction):
            if tree_height >= height:
                break
        score *= i + 1
    return score


if __name__ == "__main__":
    with open("inputs/day8.txt", "r") as FILE:
        LINES = FILE.readlines()

    TREES: list[list[int]] = []
    for line in LINES:
        TREES.append([int(char) for char in line.strip()])

    # part 1
    COUNTER = 0
    for X, TREE_LINE in enumerate(TREES):
        for Y, TREE_HEIGHT in enumerate(TREE_LINE):
            if visible(X, Y, TREE_HEIGHT, TREES):
                COUNTER += 1
    print(COUNTER)

    # part 2
    SCENIC_SCORES: list[int] = []
    for X, TREE_LINE in enumerate(TREES):
        for Y, TREE_HEIGHT in enumerate(TREE_LINE):
            SCENIC_SCORES.append(scenic_score(X, Y, TREE_HEIGHT, TREES))
    print(max(SCENIC_SCORES))
