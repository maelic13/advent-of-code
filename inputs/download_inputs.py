import os
from pathlib import Path

from aocd import get_data


# This script will download all required inputs for AoC using your personal token.
# Consult https://github.com/wimglenn/advent-of-code-data for more information.
# Edit def _limiter(self): to remove download delay
if __name__ == "__main__":
    token = (Path(__file__).parent / "token.txt").read_text(encoding="utf-8").strip()
    os.environ["AOC_SESSION"] = token

    for year in range(2019, 2026):
        for day in range(1, 26):
            file_path = Path(__file__).parent / f"{year}/day{day}.txt"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(get_data(day=day, year=year), encoding="utf-8")
