#include <algorithm>
#include <fstream>
#include <chrono>
#include <iostream>
#include <vector>
#include <tuple>

#include "infra.h"

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

    vector<tuple<string, string>> wins = {{"A", "C"}, {"B", "A"}, {"C", "B"}};
    vector<tuple<string, string>> draws = {{"A", "A"}, {"B", "B"}, {"C", "C"}};
    vector<tuple<string, string>> losses = {{"C", "A"}, {"A", "B"}, {"B", "C"}};

    int evaluate(const string& player_move, const string& opponent_move) {
        string translated_player_move = translate_move(player_move);
        int score = get_move_score(translated_player_move);
        tuple<string, string> move(translated_player_move, opponent_move);

        if (find(wins.begin(), wins.end(), move) != wins.end())
            score += win_score;
        else if (find(draws.begin(), draws.end(), move) != draws.end())
            score += draw_score;
        else
            score += lose_score;
        return score;
    }

    static string translate_move(const string& move) {
        if (move == "X" or move == "A") return "A";
        if (move == "Y" or move == "B") return "B";
        if (move == "Z" or move == "C") return "C";
        throw runtime_error("Invalid move: " + move);
    }

    [[nodiscard]] int get_move_score(const string& move) const {
        if (move == "A") return rock_score;
        if (move == "B") return paper_score;
        if (move == "C") return scissors_score;
        throw runtime_error("Invalid move: " + move);
    }

    int evaluate_with_result(const string& opponent_move, const string& result) {
        string move;

        if (result == "X") {
            for (tuple<string, string> loss : losses) {
                if (get<1>(loss) == opponent_move) {
                    move = get<0>(loss);
                    break;
                }
            }
        }
        else if (result == "Y"){
            for (tuple<string, string> draw : draws) {
                if (get<1>(draw) == opponent_move) {
                    move = get<0>(draw);
                    break;
                }
            }
        }
        else {
            for (tuple<string, string> win : wins) {
                if (get<1>(win) == opponent_move) {
                    move = get<0>(win);
                    break;
                }
            }
        }
        return evaluate(move, opponent_move);
    }
};


int main() {
    auto start = high_resolution_clock::now();

    ifstream file("year2022/inputs/day2.txt");
    string line;
    vector<vector<string>> data = {};

    while (getline(file, line))
        data.push_back(split(line, ' '));

    // part 1
    int total_score = 0;
    RPSPlayer game;
    for (auto choices: data) {
        total_score += game.evaluate(choices[1], choices[0]);
    }
    cout << total_score << endl;

    // part 2
    total_score = 0;
    for (auto inputs: data)
        total_score += game.evaluate_with_result(inputs[0], inputs[1]);
    cout << total_score << endl;

    auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start);
    cout << "Execution time: " << duration.count() << " microseconds" << endl;

    return 0;
}
