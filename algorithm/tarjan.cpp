#include <algorithm>
#include <fstream>
#include <functional>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

// Tarjan's SCC algorithm with trace emission.
//
// Emits one JSON object per line to stdout. Event types:
//   start      { n, edges }
//   enter      { v, disc, low }      -- vertex discovered
//   push       { v }                 -- vertex pushed onto stack
//   edge       { u, v, type }        -- type in {"tree","back"}
//   low_update { v, low }            -- low[v] changed
//   unstack    { v }                 -- vertex popped off stack
//   pop        { scc }               -- SCC finalized (vertices sorted)
//   finish     { scc_count }
//
// Usage: tarjan [input_file]   (default: inputs/demo.txt)

int main(int argc, char** argv) {
    std::string input_file = "inputs/demo.txt";
    if (argc > 1) input_file = argv[1];

    std::ifstream input(input_file);
    if (!input) {
        std::cerr << "Error: No se pudo abrir " << input_file << std::endl;
        return 1;
    }

    int n, m;
    if (!(input >> n >> m)) {
        std::cerr << "Error: No se pudo leer " << input_file << std::endl;
        return 1;
    }

    std::vector<std::vector<int>> graph(n);
    std::vector<std::pair<int, int>> edges;
    for (int i = 0, u, v; i < m && input >> u >> v; ++i) {
        graph[u].push_back(v);
        edges.emplace_back(u, v);
    }

    // start
    std::cout << "{\"event\":\"start\",\"n\":" << n << ",\"edges\":[";
    for (std::size_t i = 0; i < edges.size(); ++i)
        std::cout << (i ? "," : "") << "[" << edges[i].first << "," << edges[i].second << "]";
    std::cout << "]}\n";

    std::vector<int> disc(n, -1), low(n), active;
    std::vector<bool> onStack(n, false);
    int timer = 0;
    int scc_count = 0;

    std::function<void(int)> visit = [&](int v) {
        disc[v] = low[v] = timer++;
        active.push_back(v);
        onStack[v] = true;

        std::cout << "{\"event\":\"enter\",\"v\":" << v
                  << ",\"disc\":" << disc[v]
                  << ",\"low\":" << low[v] << "}\n";
        std::cout << "{\"event\":\"push\",\"v\":" << v << "}\n";

        for (int u : graph[v]) {
            if (disc[u] == -1) {
                std::cout << "{\"event\":\"edge\",\"u\":" << v
                          << ",\"v\":" << u << ",\"type\":\"tree\"}\n";
                visit(u);
                int old = low[v];
                low[v] = std::min(low[v], low[u]);
                if (low[v] != old)
                    std::cout << "{\"event\":\"low_update\",\"v\":" << v
                              << ",\"low\":" << low[v] << "}\n";
            } else if (onStack[u]) {
                std::cout << "{\"event\":\"edge\",\"u\":" << v
                          << ",\"v\":" << u << ",\"type\":\"back\"}\n";
                int old = low[v];
                low[v] = std::min(low[v], disc[u]);
                if (low[v] != old)
                    std::cout << "{\"event\":\"low_update\",\"v\":" << v
                              << ",\"low\":" << low[v] << "}\n";
            }
            // else: cross/forward edge toward an already-assigned vertex; ignored
        }

        if (low[v] == disc[v]) {
            std::vector<int> component;
            for (int u; ; ) {
                u = active.back();
                active.pop_back();
                onStack[u] = false;
                std::cout << "{\"event\":\"unstack\",\"v\":" << u << "}\n";
                component.push_back(u);
                if (u == v) break;
            }
            // Sort for clearer display in the scene summary.
            std::sort(component.begin(), component.end());
            std::cout << "{\"event\":\"pop\",\"scc\":[";
            for (std::size_t i = 0; i < component.size(); ++i)
                std::cout << (i ? "," : "") << component[i];
            std::cout << "]}\n";
            ++scc_count;
        }
    };

    for (int v = 0; v < n; ++v)
        if (disc[v] == -1) visit(v);

    std::cout << "{\"event\":\"finish\",\"scc_count\":" << scc_count << "}\n";
    return 0;
}