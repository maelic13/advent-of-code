#include <chrono>
#include <fstream>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

#include "aoc_shared.h"

using namespace std;
using namespace std::chrono;

pair<bool, size_t> is_valid(const size_t current_index,  // NOLINT(*-no-recursion)
                            const size_t current_result, const size_t expected_result,
                            const vector<size_t> &numbers,
                            const vector<function<size_t(size_t, size_t)>> &available_operands) {
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

auto count_valid(const vector<pair<size_t, vector<size_t>>> &equations,
                 const vector<function<size_t(size_t, size_t)>> &available_operands) -> size_t {
    size_t count = 0;
    for (const auto &[target, numbers] : equations) {
        if (auto [ok, res] = is_valid(1, numbers[0], target, numbers, available_operands); ok) {
            count += res;
        }
    }
    return count;
}

auto add(const size_t a, const size_t b) -> size_t { return a + b; }

auto mul(const size_t a, const size_t b) -> size_t { return a * b; }

auto con(const size_t a, const size_t b) -> size_t {
    // Instead of transfer to String and concatenate, multiply a by 10 to the power of b's
    // number of digits and add b. This is much faster.
    size_t multiplier = 10;
    while (b / multiplier > 0) {
        multiplier *= 10;
    }
    return a * multiplier + b;
}

auto parse_line(string_view input) -> pair<size_t, vector<size_t>> {
    const auto colon_pos = input.find(':');

    size_t target = 0;
    const string_view first_part = input.substr(0, colon_pos);
    from_chars(first_part.data(), first_part.data() + first_part.size(), target);

    vector<size_t> numbers;
    const string_view rest = input.substr(colon_pos + 1);
    const char *str = rest.data();
    const char *end = rest.data() + rest.size();

    while (str < end) {
        while (str < end && *str == ' ') ++str;

        size_t value = 0;
        auto [next, _] = from_chars(str, end, value);
        numbers.push_back(value);
        str = next;
    }

    return {target, numbers};
}

auto main() -> int {
    const auto start = steady_clock::now();

    // read and parse file
    ifstream file = read_input("2024", "7", false);
    vector<pair<size_t, vector<size_t>>> equations;
    string line;

    while (getline(file, line)) {
        if (line.empty()) continue;
        equations.emplace_back(parse_line(line));
    }
    const auto file_read_time = steady_clock::now() - start;

    // part 1
    const auto part1_result = count_valid(equations, {mul, add});
    const auto part1_time = steady_clock::now() - start;

    // part 2
    const auto part2_result = count_valid(equations, {mul, add, con});
    const auto part2_time = steady_clock::now() - start;

    // report results and times
    cout << part1_result << endl;
    cout << part2_result << endl;
    report_times(file_read_time, part1_time, part2_time);
}
