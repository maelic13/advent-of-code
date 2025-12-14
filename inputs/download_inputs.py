import os
from pathlib import Path

from aocd import get_data


YEAR_LENGTH = {
    2019: 25,
    2020: 25,
    2021: 25,
    2022: 25,
    2023: 25,
    2024: 25,
    2025: 12,
}


# This script will download all required inputs for AoC using your personal token.
# Consult https://github.com/wimglenn/advent-of-code-data for more information.
# Edit def _limiter(self): to remove download delay
if __name__ == "__main__":
    token = (Path(__file__).parent / "token.txt").read_text(encoding="utf-8").strip()
    os.environ["AOC_SESSION"] = token

    for year in YEAR_LENGTH:
        for day in range(1, YEAR_LENGTH[year] + 1):
            file_path = Path(__file__).parent / f"{year}/day{day}.txt"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(get_data(day=day, year=year), encoding="utf-8")
