#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "include/nlohmann/json.hpp"

using namespace std;
using json = nlohmann::json;

vector<std::pair<std::string, std::vector<string>>> vec;

void load_json(){
    ifstream f("config.json");
    if (!f.is_open()) {
        cerr << "Error: Could not open the file" << endl;
        return 1;
    }
    json data = json::parse(f);
    auto& tools = data["tools"][current_tool];

    for (const auto& tool : tools){
        cout << tool;
    }
    
}
int main(){
    load_json();
    return 0;
}