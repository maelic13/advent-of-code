#include <algorithm>
#include <fstream>
#include <chrono>
#include <iostream>
#include <numeric>
#include <vector>

using namespace std;
using namespace std::chrono;


int main() {
    const auto start = high_resolution_clock::now();

    // read and parse file
    ifstream file("inputs/2022/day1.txt");
    string line;
    vector<int> sums = {};
    int sum = 0;

    while (getline(file, line)) {
        if (line.empty()) {
            sums.push_back(sum);
            sum = 0;
            continue;
        }
        sum += stoi(line);
    }
    const auto file_read_time = duration_cast<microseconds>(
        high_resolution_clock::now() - start
        ).count();

    // part 1
    cout << *ranges::max_element(sums) << endl;
    const auto part1_time = duration_cast<microseconds>(
        high_resolution_clock::now() - start
        ).count() - file_read_time;


    //part 2
    ranges::sort(sums);
    cout << reduce(sums.end() - 3, sums.end()) << endl;
    const auto part2_time = duration_cast<microseconds>(
        high_resolution_clock::now() - start
        ).count() - part1_time - file_read_time;

    // report times
    cout << endl;
    cout << "Total time: " << file_read_time + part1_time + part2_time << " microseconds." << endl;
    cout << "File read time: " << file_read_time << " microseconds." << endl;
    cout << "Execution time: " << part1_time + part2_time << " microseconds." << endl;
    cout << endl;
    cout << "Part 1 execution time: " << part1_time << " microseconds." << endl;
    cout << "Part 2 execution time: " << part2_time << " microseconds." << endl;

    return 0;
}
