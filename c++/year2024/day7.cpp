#include <chrono>
#include <fstream>
#include <functional>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "aoc_shared.h"

// Recursive function that checks if inserting available operators
// between the numbers produces the expected result.
std::pair<bool, size_t> is_valid(
    size_t current_index, size_t current_result, size_t expected_result,
    const std::vector<size_t> &numbers,
    const std::vector<std::function<size_t(size_t, size_t)>> &available_operands) {
    if (current_index == numbers.size() || current_result > expected_result) {
        return {current_result == expected_result, current_result};
    }

    for (const auto &operand : available_operands) {
        auto [ok, res] =
            is_valid(current_index + 1, operand(current_result, numbers[current_index]),
                     expected_result, numbers, available_operands);
        if (ok) {
            return {true, res};
        }
    }
    return {false, 0};
}

// For each equation, adds the computed result if a valid operator sequence
// exists.
size_t count_valid(const std::vector<std::pair<size_t, std::vector<size_t>>> &equations,
                   const std::vector<std::function<size_t(size_t, size_t)>> &available_operands) {
    size_t count = 0;
    for (const auto &[target, numbers] : equations) {
        auto [ok, res] = is_valid(1, numbers[0], target, numbers, available_operands);
        if (ok) {
            count += res;
        }
    }
    return count;
}

size_t add(size_t a, size_t b) { return a + b; }

size_t mul(size_t a, size_t b) { return a * b; }

size_t con(size_t a, size_t b) {
    // Compute concatenation by multiplying 'a' with 10^(number of digits in b)
    // and adding b.
    size_t multiplier = 1;
    while (b / multiplier > 0) {
        multiplier *= 10;
    }
    return a * multiplier + b;
}

// Reports the elapsed times (in ms) for file reading, Part 1, and Part 2.
void report_times(const std::chrono::steady_clock::duration &file_read_time,
                  const std::chrono::steady_clock::duration &part1_time,
                  const std::chrono::steady_clock::duration &part2_time) {
    auto ms_file = std::chrono::duration_cast<std::chrono::milliseconds>(file_read_time).count();
    auto ms_part1 = std::chrono::duration_cast<std::chrono::milliseconds>(part1_time).count();
    auto ms_part2 = std::chrono::duration_cast<std::chrono::milliseconds>(part2_time).count();
    std::cout << "File Read Time: " << ms_file << " ms\n";
    std::cout << "Part 1 Time: " << ms_part1 - ms_file << " ms\n";
    std::cout << "Part 2 Time: " << ms_part2 - ms_part1 << " ms\n";
}

int main() {
    read_input();
    auto start = std::chrono::steady_clock::now();

    // Read and parse file (input file name can be adjusted as needed)
    std::ifstream infile("D:/Code/advent-of-code/inputs/2024/day7.txt");
    if (!infile) {
        std::cerr << "Error opening input file.\n";
        return 1;
    }

    std::vector<std::pair<size_t, std::vector<size_t>>> equations;
    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        auto pos = line.find(": ");
        if (pos == std::string::npos) continue;
        size_t target = std::stoull(line.substr(0, pos));
        std::string numbers_str = line.substr(pos + 2);
        std::istringstream iss(numbers_str);
        std::vector<size_t> numbers;
        size_t num;
        while (iss >> num) {
            numbers.push_back(num);
        }
        equations.emplace_back(target, numbers);
    }
    auto file_read_time = std::chrono::steady_clock::now() - start;

    // Part 1 with multiplication and addition operators
    std::vector<std::function<size_t(size_t, size_t)>> ops_part1{mul, add};
    size_t result1 = count_valid(equations, ops_part1);
    std::cout << result1 << "\n";
    auto part1_time = std::chrono::steady_clock::now() - start;

    // Part 2 with multiplication, addition, and concatenation operators
    std::vector<std::function<size_t(size_t, size_t)>> ops_part2{mul, add, con};
    size_t result2 = count_valid(equations, ops_part2);
    std::cout << result2 << "\n";
    auto part2_time = std::chrono::steady_clock::now() - start;

    // Report times
    report_times(file_read_time, part1_time, part2_time);

    return 0;
}
