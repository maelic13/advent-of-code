from .constants import Constants


def read_input(year: int, day: int, *, example: bool) -> str:
    suffix = "_ex" if example else ""
    return (Constants.INPUT_PATH / f"{year}/day{day}{suffix}.txt").read_text(encoding="utf-8")
