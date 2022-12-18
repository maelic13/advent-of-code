#include <sstream>
#include <vector>

using namespace std;

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

vector<int> to_int(const vector<string>& str_vec) {
    vector<int> int_vec = {};
    for (const string& element: str_vec)
        int_vec.push_back(stoi(element));
    return int_vec;
}
