#include <algorithm>
#include <fstream>
#include <chrono>
#include <iostream>
#include <vector>
#include <tuple>

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

    int evaluate(const char opponent_move, char player_move) {
        player_move = translate_move(player_move);
        int score = get_move_score(player_move);
        tuple<char, char> move(player_move, opponent_move);

        if (find(wins.begin(), wins.end(), move) != wins.end())
            score += win_score;
        else if (find(draws.begin(), draws.end(), move) != draws.end())
            score += draw_score;
        else
            score += lose_score;
        return score;
    }

    static char translate_move(const char move) {
        if (move == 'X' or move == 'A') return 'A';
        if (move == 'Y' or move == 'B') return 'B';
        if (move == 'Z' or move == 'C') return 'C';
        throw runtime_error(&"Invalid move: " [move]);
    }

    [[nodiscard]] int get_move_score(char move) const {
        if (move == 'A') return rock_score;
        if (move == 'B') return paper_score;
        if (move == 'C') return scissors_score;
        throw runtime_error(&"Invalid move: " [move]);
    }

    int evaluate_with_result(const char opponent_move, const char result) {
        char move;

        if (result == 'X') {
            for (tuple<char, char> loss : losses) {
                if (get<1>(loss) == opponent_move) {
                    move = get<0>(loss);
                    break;
                }
            }
        }
        else if (result == 'Y'){
            for (tuple<char, char> draw : draws) {
                if (get<1>(draw) == opponent_move) {
                    move = get<0>(draw);
                    break;
                }
            }
        }
        else {
            for (tuple<char, char> win : wins) {
                if (get<1>(win) == opponent_move) {
                    move = get<0>(win);
                    break;
                }
            }
        }
        return evaluate(opponent_move, move);
    }
};


int main() {
    auto start = high_resolution_clock::now();

    // read and parse file
    ifstream file("inputs/2022/day2.txt");
    string line;
    vector<string> data;

    while (getline(file, line)) {
        string item;
        const char* currentChar = line.c_str();

        for (int i = 0; i < 3; i++) {
            if (*currentChar != ' ')
                item += *currentChar;
            *currentChar++;
        }
        data.push_back(item);
    }
    auto file_read_time = duration_cast<microseconds>(high_resolution_clock::now() - start).count();

    // part 1
    int total_score = 0;
    RPSPlayer game;
    for (auto choices: data) {
        total_score += game.evaluate(choices[0], choices[1]);
    }
    auto part1_time = duration_cast<microseconds>(high_resolution_clock::now() - start).count() - file_read_time;
    cout << total_score << endl;

    // part 2
    total_score = 0;
    for (auto inputs: data)
        total_score += game.evaluate_with_result(inputs[0], inputs[1]);
    auto part2_time = duration_cast<microseconds>(high_resolution_clock::now() - start).count() - part1_time - file_read_time;
    cout << total_score << endl;

    cout << endl;
    cout << "Total time: " << file_read_time + part1_time + part2_time << " microseconds." << endl;
    cout << "File read time: " << file_read_time << " microseconds." << endl;
    cout << "Execution time: " << part1_time + part2_time << " microseconds." << endl;
    cout << endl;
    cout << "Part 1 execution time: " << part1_time << " microseconds." << endl;
    cout << "Part 2 execution time: " << part2_time << " microseconds." << endl;

    return 0;
}
