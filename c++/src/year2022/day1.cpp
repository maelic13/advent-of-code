#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>

#include "aoc_shared.h"

using namespace std;
using namespace std::chrono;

auto main() -> int {
    const auto start = steady_clock::now();

    // read and parse file
    ifstream file = read_input("2022", "1", false);
    vector<int> sums = {};
    int sum = 0;

    string line;
    while (getline(file, line)) {
        if (line.empty()) {
            sums.push_back(sum);
            sum = 0;
            continue;
        }
        sum += stoi(line);
    }
    const auto file_read_time = steady_clock::now() - start;

    // part 1
    const auto part1_result = *ranges::max_element(sums);
    const auto part1_time = steady_clock::now() - start;

    // part 2
    ranges::sort(sums);
    const auto part2_result = reduce(sums.end() - 3, sums.end());
    const auto part2_time = steady_clock::now() - start;

    // report results and times
    cout << part1_result << endl;
    cout << part2_result << endl;
    report_times(file_read_time, part1_time, part2_time);
}
