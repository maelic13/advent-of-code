#include <algorithm>
#include <fstream>
#include <chrono>
#include <iostream>
#include <numeric>
#include <vector>

using namespace std;
using namespace std::chrono;


int main() {
    auto start = high_resolution_clock::now();

    ifstream file("year2022/inputs/day1.txt");
    string line;
    vector<vector<int>> elves_calories = {{}};

    while (getline(file, line)) {
        if (line.empty()) {
            elves_calories.emplace_back();
            continue;
        }
        elves_calories.back().push_back(stoi(line));
    }

    // part 1
    vector<int> sums = {};
    for (vector<int> calories: elves_calories)
        sums.push_back(reduce(calories.begin(), calories.end()));
    cout << *max_element(sums.begin(), sums.end()) << endl;

    //part 2
    sort(sums.begin(), sums.end());
    cout << reduce(sums.end() - 3, sums.end()) << endl;

    auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start);
    cout << "Execution time: " << duration.count() << " microseconds" << endl;

    return 0;
}
