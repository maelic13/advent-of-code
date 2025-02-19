#include <chrono>
#include <format>
#include <iostream>
#include <string>

#ifdef _WIN32
#include <windows.h>
#endif

using namespace std::chrono;

auto formatDuration(const steady_clock::duration& duration) -> std::string {
    double seconds = std::chrono::duration<double>(duration).count();
    if (seconds >= 1.0) {
        return std::format("{:.1f}s", seconds);
    }
    if (seconds * 1e3 >= 1.0) {
        return std::format("{:.1f}ms", seconds * 1000);
    }
    if (seconds * 1e6 >= 1.0) {
        return std::format("{:.1f}µs", seconds * 1e6);
    }
    return std::format("{:.1f}ns", seconds * 1e9);
}

auto saturating_sub(const steady_clock::duration& a, const steady_clock::duration& b)
    -> steady_clock::duration {
    return a > b ? a - b : steady_clock::duration::zero();
}

auto report_times(const steady_clock::duration& file_parse_time,
                  const steady_clock::duration& part1_time,
                  const steady_clock::duration& part2_time) -> void {
#ifdef _WIN32
    // Set Windows console to UTF-8
    SetConsoleOutputCP(CP_UTF8);
#endif

    const auto execution_time = saturating_sub(part2_time, file_parse_time);
    const auto only_part1_time = saturating_sub(part1_time, file_parse_time);
    const auto only_part2_time = saturating_sub(part2_time, part1_time);

    std::cout << std::endl;
    std::cout << std::format("Total time: {}.\n", formatDuration(part2_time));
    std::cout << std::format("File read time: {}.\n", formatDuration(file_parse_time));
    std::cout << std::format("Execution time: {}.\n", formatDuration(execution_time));
    std::cout << std::endl;
    std::cout << std::format("Part 1 execution time: {}.\n", formatDuration(only_part1_time));
    std::cout << std::format("Part 2 execution time: {}.\n", formatDuration(only_part2_time));
}
