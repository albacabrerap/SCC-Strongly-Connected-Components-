#include <algorithm>
#include <cassert>
#include <initializer_list>
#include <string>
#include <vector>

#include "graph.hpp"
#include "tarjan.hpp"

namespace {

std::vector<std::vector<int>> normalize(const std::vector<std::vector<int>>& components) {
    std::vector<std::vector<int>> normalized = components;
    for (auto& component : normalized) {
        std::sort(component.begin(), component.end());
    }
    std::sort(normalized.begin(), normalized.end(), [](const std::vector<int>& a, const std::vector<int>& b) {
        if (a.empty() && b.empty()) {
            return false;
        }
        if (a.empty()) {
            return true;
        }
        if (b.empty()) {
            return false;
        }
        return a.front() < b.front();
    });
    return normalized;
}

void expect_case(const std::string& path, const std::vector<std::vector<int>>& expected) {
    Graph graph = Graph::from_file(path);
    TarjanSolver solver(graph);
    const auto result = normalize(solver.run());
    assert(result == normalize(expected));
}

}  // namespace

int main() {
    expect_case("data/empty.txt", {});
    expect_case("data/single.txt", {{0}});
    expect_case("data/dag.txt", {{0}, {1}, {2}, {3}});
    expect_case("data/selfloop.txt", {{0}});
    expect_case("data/full_cycle.txt", {{0, 1, 2, 3}});
    expect_case("data/demo.txt", {{0, 1, 2}, {3, 4, 5}, {6, 7}});
    return 0;
}
