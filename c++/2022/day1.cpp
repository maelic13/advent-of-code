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

    // part 1
    cout << *max_element(sums.begin(), sums.end()) << endl;

    //part 2
    sort(sums.begin(), sums.end());
    cout << reduce(sums.end() - 3, sums.end()) << endl;

    auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start);
    cout << "Execution time: " << duration.count() << " microseconds." << endl;

    return 0;
}
