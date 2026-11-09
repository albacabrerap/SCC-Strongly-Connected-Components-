#include <iostream>
#include <string>
#include <vector>

#include "graph.hpp"
#include "tarjan.hpp"

int main(int argc, char* argv[]) {
    std::string input_path = "data/demo.txt";
    if (argc > 1) {
        input_path = argv[1];
    }

    try {
        Graph graph = Graph::from_file(input_path);
        TarjanSolver solver(graph);
        std::vector<std::vector<int>> components = solver.run();
        (void)components;
        return 0;
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << '\n';
        return 1;
    }
}
