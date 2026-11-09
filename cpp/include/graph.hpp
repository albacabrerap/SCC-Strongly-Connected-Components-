#pragma once

#include <cstddef>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class Graph {
public:
    explicit Graph(std::size_t n = 0);

    std::size_t node_count() const noexcept;
    const std::vector<std::vector<int>>& adjacency() const noexcept;
    const std::vector<std::pair<int, int>>& edges() const noexcept;

    void add_edge(int u, int v);

    static Graph from_file(const std::string& path);

private:
    std::size_t n_;
    std::vector<std::vector<int>> adjacency_;
    std::vector<std::pair<int, int>> edges_;
};
