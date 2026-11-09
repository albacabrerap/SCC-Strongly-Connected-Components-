#include "graph.hpp"

#include <fstream>
#include <sstream>
#include <string>
#include <utility>

Graph::Graph(std::size_t n)
    : n_(n), adjacency_(n), edges_() {}

std::size_t Graph::node_count() const noexcept {
    return n_;
}

const std::vector<std::vector<int>>& Graph::adjacency() const noexcept {
    return adjacency_;
}

const std::vector<std::pair<int, int>>& Graph::edges() const noexcept {
    return edges_;
}

void Graph::add_edge(int u, int v) {
    if (u < 0 || v < 0 || static_cast<std::size_t>(u) >= n_ || static_cast<std::size_t>(v) >= n_) {
        throw std::out_of_range("Edge endpoint out of range.");
    }
    adjacency_[u].push_back(v);
    edges_.emplace_back(u, v);
}

Graph Graph::from_file(const std::string& path) {
    std::ifstream input(path);
    if (!input.is_open()) {
        throw std::runtime_error("No se pudo abrir el archivo: " + path);
    }

    std::string line;
    int n = 0;
    int m = 0;
    bool header_read = false;

    Graph graph(0);

    while (std::getline(input, line)) {
        std::stringstream ss(line);
        std::string token;

        if (line.find('#') != std::string::npos) {
            line = line.substr(0, line.find('#'));
        }

        if (line.empty()) {
            continue;
        }

        std::vector<std::string> parts;
        while (ss >> token) {
            parts.push_back(token);
        }

        if (!header_read) {
            if (parts.size() != 2) {
                throw std::runtime_error("La primera línea debe contener 'n m'.");
            }
            n = std::stoi(parts[0]);
            m = std::stoi(parts[1]);
            graph = Graph(static_cast<std::size_t>(n));
            header_read = true;
            continue;
        }

        if (parts.size() != 2) {
            throw std::runtime_error("Cada arista debe tener exactamente dos nodos.");
        }

        int u = std::stoi(parts[0]);
        int v = std::stoi(parts[1]);
        graph.add_edge(u, v);
    }

    if (!header_read) {
        throw std::runtime_error("Falta la línea de cabecera 'n m'.");
    }

    if (static_cast<int>(graph.edges().size()) != m) {
        throw std::runtime_error("Cantidad de aristas distinta a la cabecera.");
    }

    return graph;
}
