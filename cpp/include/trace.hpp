#pragma once

#include <string>
#include <utility>
#include <vector>

namespace trace {

void emit_event_start(int step, int n, int m, const std::vector<std::pair<int, int>>& edges,
                      const std::string& caption);
void emit_event_dfs_enter(int step, int v, int disc, int low, const std::vector<int>& stack,
                         const std::string& caption);
void emit_event_edge(int step, int u, int v, const std::string& kind, const std::string& caption);
void emit_event_low_update(int step, int v, int new_low, int via, const std::string& caption);
void emit_event_dfs_exit(int step, int v, int disc, int low, const std::string& caption);
void emit_event_scc_pop(int step, const std::vector<int>& nodes, int scc_id, const std::string& caption);
void emit_event_end(int step, const std::vector<std::vector<int>>& sccs, const std::string& caption);

}  // namespace trace
