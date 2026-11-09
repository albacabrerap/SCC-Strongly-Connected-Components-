#include "trace.hpp"

#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace trace {

std::string json_escape(const std::string& value) {
    std::ostringstream out;
    for (char ch : value) {
        switch (ch) {
            case '"': out << "\\\""; break;
            case '\\': out << "\\\\"; break;
            case '\n': out << "\\n"; break;
            case '\r': out << "\\r"; break;
            case '\t': out << "\\t"; break;
            default:
                if (static_cast<unsigned char>(ch) < 0x20) {
                    out << "\\u" << std::hex << std::setw(4) << std::setfill('0')
                        << static_cast<int>(static_cast<unsigned char>(ch)) << std::dec;
                } else {
                    out << ch;
                }
                break;
        }
    }
    return out.str();
}

std::string format_vector(const std::vector<int>& values) {
    std::ostringstream out;
    out << "[";
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i > 0) {
            out << ",";
        }
        out << values[i];
    }
    out << "]";
    return out.str();
}

std::string format_matrix(const std::vector<std::vector<int>>& values) {
    std::ostringstream out;
    out << "[";
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i > 0) {
            out << ",";
        }
        out << format_vector(values[i]);
    }
    out << "]";
    return out.str();
}

std::string format_edges(const std::vector<std::pair<int, int>>& edges) {
    std::ostringstream out;
    out << "[";
    for (std::size_t i = 0; i < edges.size(); ++i) {
        if (i > 0) {
            out << ",";
        }
        out << "[" << edges[i].first << "," << edges[i].second << "]";
    }
    out << "]";
    return out.str();
}

void emit_event_start(int step, int n, int m, const std::vector<std::pair<int, int>>& edges,
                      const std::string& caption) {
    std::cout << "{\"step\":" << step << ",\"event\":\"start\",\"n\":" << n
              << ",\"m\":" << m << ",\"edges\":" << format_edges(edges)
              << ",\"caption\":\"" << json_escape(caption) << "\"}\n";
}

void emit_event_dfs_enter(int step, int v, int disc, int low, const std::vector<int>& stack,
                         const std::string& caption) {
    std::cout << "{\"step\":" << step << ",\"event\":\"dfs_enter\",\"v\":" << v
              << ",\"disc\":" << disc << ",\"low\":" << low << ",\"stack\":"
              << format_vector(stack) << ",\"caption\":\"" << json_escape(caption) << "\"}\n";
}

void emit_event_edge(int step, int u, int v, const std::string& kind, const std::string& caption) {
    std::cout << "{\"step\":" << step << ",\"event\":\"edge\",\"u\":" << u
              << ",\"v\":" << v << ",\"kind\":\"" << kind << "\",\"caption\":\""
              << json_escape(caption) << "\"}\n";
}

void emit_event_low_update(int step, int v, int new_low, int via, const std::string& caption) {
    std::cout << "{\"step\":" << step << ",\"event\":\"low_update\",\"v\":" << v
              << ",\"new_low\":" << new_low << ",\"via\":" << via
              << ",\"caption\":\"" << json_escape(caption) << "\"}\n";
}

void emit_event_dfs_exit(int step, int v, int disc, int low, const std::string& caption) {
    std::cout << "{\"step\":" << step << ",\"event\":\"dfs_exit\",\"v\":" << v
              << ",\"disc\":" << disc << ",\"low\":" << low
              << ",\"caption\":\"" << json_escape(caption) << "\"}\n";
}

void emit_event_scc_pop(int step, const std::vector<int>& nodes, int scc_id, const std::string& caption) {
    std::cout << "{\"step\":" << step << ",\"event\":\"scc_pop\",\"nodes\":"
              << format_vector(nodes) << ",\"scc_id\":" << scc_id << ",\"caption\":\""
              << json_escape(caption) << "\"}\n";
}

void emit_event_end(int step, const std::vector<std::vector<int>>& sccs, const std::string& caption) {
    std::cout << "{\"step\":" << step << ",\"event\":\"end\",\"sccs\":"
              << format_matrix(sccs) << ",\"caption\":\"" << json_escape(caption) << "\"}\n";
}

}  // namespace trace
