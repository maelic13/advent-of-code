#include <chrono>
#include <fstream>
#include <iostream>
#include <tuple>
#include <vector>

#include "aoc_shared.h"

using namespace std;
using namespace std::chrono;

class RPSPlayer {
   public:
    int win_score = 6;
    int draw_score = 3;
    int lose_score = 0;

    int rock_score = 1;
    int paper_score = 2;
    int scissors_score = 3;

    vector<tuple<char, char>> wins = {{'A', 'C'}, {'B', 'A'}, {'C', 'B'}};
    vector<tuple<char, char>> draws = {{'A', 'A'}, {'B', 'B'}, {'C', 'C'}};
    vector<tuple<char, char>> losses = {{'C', 'A'}, {'A', 'B'}, {'B', 'C'}};

    auto evaluate(const char opponent_move, char player_move) -> int {
        player_move = translate_move(player_move);
        int score = get_move_score(player_move);

        if (const tuple move(player_move, opponent_move); ranges::find(wins, move) != wins.end())
            score += win_score;
        else if (ranges::find(draws, move) != draws.end())
            score += draw_score;
        else if (ranges::find(losses, move) != losses.end())
            score += lose_score;
        else
            throw runtime_error("Incorrect move vector.");
        return score;
    }

    auto evaluate_with_result(const char opponent_move, const char result) -> int {
        char player_move = 0;
        vector<tuple<char, char>>* to_search;

        if (result == 'X') {
            to_search = &losses;
        } else if (result == 'Y') {
            to_search = &draws;
        } else if (result == 'Z') {
            to_search = &wins;
        } else {
            throw runtime_error("Incorrect result: " + to_string(result));
        }

        for (tuple game_result : *to_search)
            if (get<1>(game_result) == opponent_move) {
                player_move = get<0>(game_result);
                break;
            }

        return evaluate(opponent_move, player_move);
    }

    static auto translate_move(const char move) -> char {
        if (move == 'X' or move == 'A') return 'A';
        if (move == 'Y' or move == 'B') return 'B';
        if (move == 'Z' or move == 'C') return 'C';
        throw runtime_error("Invalid move: " + to_string(move));
    }

    [[nodiscard]] auto get_move_score(const char move) const -> int {
        if (move == 'A') return rock_score;
        if (move == 'B') return paper_score;
        if (move == 'C') return scissors_score;
        throw runtime_error("Invalid move: " + to_string(move));
    }
};

auto main() -> void {
    auto start = steady_clock::now();

    // read and parse file
    ifstream file = read_input("2022", "2", false);
    string line;
    vector<string> data;

    while (getline(file, line)) {
        string item;
        const char* currentChar = line.c_str();

        for (int i = 0; i < 3; i++) {
            if (*currentChar != ' ') item += *currentChar;
            *currentChar++;
        }
        data.push_back(item);
    }
    auto file_read_time = steady_clock::now() - start;

    // part 1
    auto part1_result = 0;
    RPSPlayer game;
    for (auto choices : data) {
        part1_result += game.evaluate(choices[0], choices[1]);
    }
    auto part1_time = steady_clock::now() - start;

    // part 2
    auto part2_result = 0;
    for (auto inputs : data) part2_result += game.evaluate_with_result(inputs[0], inputs[1]);
    auto part2_time = steady_clock::now() - start;

    // report results and times
    cout << part1_result << endl;
    cout << part2_result << endl;
    report_times(file_read_time, part1_time, part2_time);
}
