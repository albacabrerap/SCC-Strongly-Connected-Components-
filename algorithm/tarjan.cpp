#include <algorithm>
#include <fstream>
#include <functional>
#include <iostream>
#include <utility>
#include <vector>

int main() {
    std::ifstream input("inputs/demo.txt");
    int n, m;
    if (!(input >> n >> m)) {
    std::cerr << "Error: No se pudo leer inputs/demo.txt" << std::endl;
    return 1;
}

    std::vector<std::vector<int>> graph(n);
    std::vector<std::pair<int, int>> edges;
    for (int i = 0, u, v; i < m && input >> u >> v; ++i) {
        graph[u].push_back(v);
        edges.emplace_back(u, v);
    }
    std::cout << "{\"event\":\"start\",\"n\":" << n << ",\"edges\":[";
    for (std::size_t i = 0; i < edges.size(); ++i)
        std::cout << (i ? "," : "") << "[" << edges[i].first << "," << edges[i].second << "]";
    std::cout << "]}\n";

    std::vector<int> disc(n, -1), low(n), active;
    std::vector<bool> onStack(n, false);
    int timer = 0;
    std::function<void(int)> visit = [&](int v) {
        disc[v] = low[v] = timer++;
        active.push_back(v);
        onStack[v] = true;
        std::cout << "{\"event\":\"enter\",\"v\":" << v << ",\"disc\":" << disc[v] << ",\"low\":" << low[v] << "}\n";
        for (int u : graph[v]) {
            if (disc[u] == -1) {
                std::cout << "{\"event\":\"edge\",\"u\":" << v << ",\"v\":" << u << ",\"type\":\"tree\"}\n";
                visit(u);
                low[v] = std::min(low[v], low[u]);
            } else if (onStack[u]) {
                std::cout << "{\"event\":\"edge\",\"u\":" << v << ",\"v\":" << u << ",\"type\":\"back\"}\n";
                low[v] = std::min(low[v], disc[u]);
            }
        }
        if (low[v] == disc[v]) {
            std::vector<int> component;
            for (int u; ; ) {
                u = active.back(); active.pop_back(); onStack[u] = false; component.push_back(u);
                if (u == v) break;
            }
            std::cout << "{\"event\":\"pop\",\"scc\":[";
            for (std::size_t i = 0; i < component.size(); ++i)
                std::cout << (i ? "," : "") << component[i];
            std::cout << "]}\n";
        }
    };
    for (int v = 0; v < n; ++v) if (disc[v] == -1) visit(v);
}