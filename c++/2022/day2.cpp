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


vector<string> split(const string& line, char delimiter) {
    stringstream stream(line);
    string word;
    vector<string> parsed = {};

    while (!stream.eof()) {
        getline(stream, word, delimiter);
        parsed.push_back(word);
    }
    return parsed;
}


int main() {
    auto start = high_resolution_clock::now();

    ifstream file("inputs/2022/day2.txt");
    string line;
    vector<vector<string>> data = {};

    while (getline(file, line))
        data.push_back(split(line, ' '));
    auto file_read_time = duration_cast<microseconds>(high_resolution_clock::now() - start).count();

    // part 1
    int total_score = 0;
    RPSPlayer game;
    for (auto choices: data) {
        total_score += game.evaluate(choices[1], choices[0]);
    }
    auto part1_time = duration_cast<microseconds>(high_resolution_clock::now() - start).count() - file_read_time;
    cout << total_score << endl;

    // part 2
    total_score = 0;
    for (auto inputs: data)
        total_score += game.evaluate_with_result(inputs[0], inputs[1]);
    auto part2_time = duration_cast<microseconds>(high_resolution_clock::now() - start).count() - part1_time - file_read_time;
    cout << total_score << endl;

    auto total_time = duration_cast<microseconds>(high_resolution_clock::now() - start).count();
    cout << endl;
    cout << "Total time: " << total_time << " microseconds." << endl;
    cout << "File read time: " << file_read_time << " microseconds." << endl;
    cout << "Execution time: " << part1_time + part2_time << " microseconds." << endl;
    cout << endl;
    cout << "Part 1 execution time: " << part1_time << " microseconds." << endl;
    cout << "Part 2 execution time: " << part2_time << " microseconds." << endl;

    return 0;
}
