#include <iostream> 
#include <fstream> 
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <cmath> 
#include <chrono>
#include <algorithm>
#include <limits>

using namespace std;
const float MAX_STEP_SIZE = 1.5f;

struct Point {
    int x, y;
    bool operator==(const Point& other) const { // == operator override
        return x == other.x && y == other.y;
    }
    bool operator!=(const Point& other) const { // != operator override
        return !(*this == other);
    }
};

struct PointHash{
    size_t operator()(const Point& p) const {
        return (size_t)p.y * 10000 + (size_t)p.x;
    }
};

struct Node {
    Point Point;
    float f_score;
    bool operator>(const Node& other) const { // > operator override
        return f_score > other.f_score;
    }
};


float distance_between_points(Point p1, Point p2){ //p1 is current, p2 is neighbor
    float dx = p1.x - p2.x;
    float dy = p1.y - p2.y;
    return sqrt(dx * dx + dy * dy);
}

unordered_map<Point, float, PointHash> read_csv(const string& filename){
    unordered_map<Point, float, PointHash> costs_dict;
    ifstream file(filename);
    string line;

    getline(file, line); 
    while(getline(file,line)){
        stringstream ss(line);
        string str;
        Point point;
        float cost;

        getline(ss, str, ','); 
        point.x = static_cast<int>(stod(str));
        getline(ss, str, ',');
        point.y = static_cast<int>(stod(str));
        getline(ss, str, ',');
        cost = stof(str);
        costs_dict[point] = cost;
    }
    return costs_dict;
}

vector<Point> pathfinding(Point start, Point goal, const unordered_map<Point, float, PointHash>& costs_dict){
    
    priority_queue<Node, vector<Node>, greater<Node>> open_list;
    unordered_set<Point, PointHash> closed_list;
    unordered_map<Point, Point, PointHash> came_from;

    unordered_map<Point, float, PointHash> g_score;
    unordered_map<Point, float, PointHash> f_score;

    for (const auto& pair : costs_dict) {

    g_score[pair.first] = numeric_limits<float>::infinity();
    f_score[pair.first] = numeric_limits<float>::infinity();

    }

    g_score[start] = 0.0f;
    f_score[start] = distance_between_points(start, goal);
    open_list.push({start, f_score[start]});

    Point directions[8] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1},{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};

    while (!open_list.empty()){

        Point current = open_list.top().Point;
        open_list.pop();

        if (closed_list.count(current)){
            continue;
        }

        if(current == goal){
            vector<Point> path;
            while (current != start){
                path.push_back(current);
                current = came_from[current];
            }
            path.push_back(start);
            reverse(path.begin(), path.end());
            return path;
        }
        closed_list.insert(current);

        for (const auto& dir : directions){

            Point neighbor = {current.x + dir.x, current.y + dir.y};

            if (costs_dict.find(neighbor) == costs_dict.end()){
                continue;
            }

            if (closed_list.count(neighbor)){
                continue;
            }

            float step_cost = distance_between_points(current, neighbor);
            if (step_cost > MAX_STEP_SIZE){
                continue;
            }

            float neighbor_cost = costs_dict.at(neighbor);
            float tentative_g_score = g_score[current] + neighbor_cost + step_cost;

            if (tentative_g_score < g_score[neighbor]){
                came_from[neighbor] = current;
                g_score[neighbor] = tentative_g_score;
                f_score[neighbor] = g_score[neighbor] + distance_between_points(neighbor, goal);

                if (closed_list.count(neighbor)){
                    closed_list.erase(neighbor);
                }

                open_list.push({neighbor, f_score[neighbor]});
            }

        }

    }


    return {};

}

int main(int argc, char* argv[]){
    if (argc < 3) {
        std::cerr << "Nie podano ścieżki" << std::endl;
        return 1;
    }
    string sciezka_do_csv = argv[1];
    string csv = sciezka_do_csv;
    int cord = stoi(argv[2]);

    Point start = {0, cord - 1};
    Point goal = {cord - 1, 0};

    auto costs_dict = read_csv(csv);

    auto start_time = chrono::high_resolution_clock::now();

    cout << "Started Pathfinding in CPP" << endl;

    vector<Point> path = pathfinding(start, goal, costs_dict);

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end_time - start_time;

    cout << "Completed in " << elapsed.count() << " seconds." << endl;


    if (!path.empty()){
        cout << "Path found with " << path.size() << " points." << endl;
        ofstream output_file("path_output.csv");
        output_file << "x,y\n";
        for (const auto& point : path){
            output_file << point.x << "," << point.y << "\n";
        }
        output_file.close();
    } else {
        cout << "No path found." << endl;
    }



    return 0;
}