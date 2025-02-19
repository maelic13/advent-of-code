#include <filesystem>
#include <fstream>
#include <stdexcept>
#include <string>

using namespace std;
using namespace std::filesystem;

auto get_input_path() -> path {
    path current = current_path();
    while (true) {
        if (exists(current / "inputs") && is_directory(current / "inputs"))
            return current / "inputs";

        if (current.has_parent_path())
            current = current.parent_path();
        else
            break;
    }
    throw runtime_error("Inputs not found.");
}

auto read_input(const string& year, const string& day, const bool example) -> ifstream {
    const std::string suffix = example ? "_ex" : "";
    const path filePath = get_input_path() / year / ("day" + day + suffix + ".txt");

    ifstream file(filePath);
    if (!file)
        throw runtime_error("Failed to open file: " + filePath.string());
    return file;
}
