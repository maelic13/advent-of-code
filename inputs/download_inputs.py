import os
from pathlib import Path

from aocd import get_data


# This script will download all required inputs for AoC using your personal token.
# Consult https://github.com/wimglenn/advent-of-code-data for more information.
# Edit def _limiter(self): to remove download delay
if __name__ == "__main__":
    with open("token.txt", "r") as token_file:
        token = token_file.read().strip()
    os.environ["AOC_SESSION"] = token

    for year in range(2019, 2024):
        for day in range(1, 26):
            file_path = Path(f"{year}/day{day}.txt")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as f:
                f.write(get_data(day=day, year=year))
