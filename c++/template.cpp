#include <fstream>
#include <iostream>

#include "aoc_shared.h"

using namespace std;
using namespace std::chrono;

auto main() -> int {
    const auto start = steady_clock::now();

    // read and parse file
    ifstream file = read_input("2024", "1", true);
    string line;
    while (getline(file, line)) {
        if (line.empty()) continue;
    }
    const auto file_read_time = steady_clock::now() - start;

    // part 1
    auto part1_result = 0;
    const auto part1_time = steady_clock::now() - start;

    // part 2
    auto part2_result = 0;
    const auto part2_time = steady_clock::now() - start;

    // report results and times
    cout << part1_result << endl;
    cout << part2_result << endl;
    report_times(file_read_time, part1_time, part2_time);
}
