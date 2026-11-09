#pragma once

#include <string>
#include <vector>

#include "graph.hpp"

class TarjanSolver {
public:
    explicit TarjanSolver(const Graph& graph);

    std::vector<std::vector<int>> run();

private:
    void dfs(int v);
    void emit_trace_start() const;
    void emit_trace_dfs_enter(int v) const;
    void emit_trace_edge(int u, int v, const std::string& kind, const std::string& caption) const;
    void emit_trace_low_update(int v, int new_low, int via, const std::string& caption) const;
    void emit_trace_dfs_exit(int v) const;
    void emit_trace_scc_pop(const std::vector<int>& component, int scc_id) const;
    void emit_trace_end() const;

    const Graph& graph_;
    std::vector<int> disc_;
    std::vector<int> low_;
    std::vector<int> stack_;
    std::vector<int> on_stack_;
    std::vector<std::vector<int>> components_;
    int timer_ = 0;
    mutable int step_counter_ = 0;
};
