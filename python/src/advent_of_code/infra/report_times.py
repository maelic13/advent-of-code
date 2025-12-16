def report_times(file_read_time: int, part1_time: int, part2_time: int) -> None:
    """
    Report execution times with automatically selected units.

    Args:
        file_read_time: Time in nanoseconds after file reading
        part1_time: Time in nanoseconds after part 1 completion
        part2_time: Time in nanoseconds after part 2 completion
    """
    print()
    print(f"Total time: {format_duration(part2_time)}.")
    print(f"File read time: {format_duration(file_read_time)}.")
    print(f"Execution time: {format_duration(part2_time - file_read_time)}.")
    print()
    print(f"Part 1 execution time: {format_duration(part1_time - file_read_time)}.")
    print(f"Part 2 execution time: {format_duration(part2_time - part1_time)}.")


def format_duration(nanoseconds: int) -> str:
    """
    Format nanoseconds into human-readable duration with appropriate unit.
    """
    if nanoseconds < 1_000:
        return f"{nanoseconds}ns"
    if nanoseconds < 1_000_000:
        return f"{nanoseconds / 1_000:.1f}μs"
    if nanoseconds < 1_000_000_000:
        return f"{nanoseconds / 1_000_000:.1f}ms"
    if nanoseconds < 60_000_000_000:
        return f"{nanoseconds / 1_000_000_000:.1f}s"
    if nanoseconds < 3_600_000_000_000:
        minutes = nanoseconds / 60_000_000_000
        return f"{minutes:.1f}min"
    hours = nanoseconds / 3_600_000_000_000
    return f"{hours:.1f}h"
