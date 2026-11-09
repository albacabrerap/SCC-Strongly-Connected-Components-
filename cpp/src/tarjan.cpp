#include "tarjan.hpp"

#include <algorithm>
#include <string>
#include <utility>
#include <vector>

#include "trace.hpp"

TarjanSolver::TarjanSolver(const Graph& graph)
    : graph_(graph),
      disc_(graph.node_count(), -1),
      low_(graph.node_count(), 0),
      stack_(),
      on_stack_(graph.node_count(), 0),
      components_() {}

std::vector<std::vector<int>> TarjanSolver::run() {
    emit_trace_start();
    for (std::size_t v = 0; v < graph_.node_count(); ++v) {
        if (disc_[v] == -1) {
            dfs(static_cast<int>(v));
        }
    }
    emit_trace_end();
    return components_;
}

void TarjanSolver::dfs(int v) {
    disc_[v] = timer_;
    low_[v] = timer_;
    timer_ += 1;

    stack_.push_back(v);
    on_stack_[v] = 1;

    emit_trace_dfs_enter(v);

    for (int neighbor : graph_.adjacency()[v]) {
        const std::string kind = disc_[neighbor] == -1 ? "tree" : (on_stack_[neighbor] ? "back" : "cross");
        const std::string caption = kind == "tree"
            ? "Se explora una arista de expansión y se sigue el recorrido en profundidad."
            : (kind == "back" ? "La arista retrocede a un nodo activo en la pila y actualiza el valor low." : "La arista cruza un componente ya cerrado y se ignora.");

        emit_trace_edge(v, neighbor, kind, caption);

        if (disc_[neighbor] == -1) {
            dfs(neighbor);
            low_[v] = std::min(low_[v], low_[neighbor]);
            if (low_[v] != disc_[v]) {
                emit_trace_low_update(v, low_[v], neighbor, "Se mejora low del nodo actual usando el retorno del vecino.");
            }
        } else if (on_stack_[neighbor]) {
            low_[v] = std::min(low_[v], disc_[neighbor]);
            emit_trace_low_update(v, low_[v], neighbor, "Se actualiza low con una arista de retorno hacia la pila abierta.");
        }
    }

    if (low_[v] == disc_[v]) {
        std::vector<int> component;
        while (true) {
            int w = stack_.back();
            stack_.pop_back();
            on_stack_[w] = 0;
            component.push_back(w);
            if (w == v) {
                break;
            }
        }

        std::sort(component.begin(), component.end());
        components_.push_back(component);
        emit_trace_scc_pop(component, static_cast<int>(components_.size()) - 1);
    }

    emit_trace_dfs_exit(v);
}

void TarjanSolver::emit_trace_start() const {
    trace::emit_event_start(++step_counter_, static_cast<int>(graph_.node_count()),
                            static_cast<int>(graph_.edges().size()), graph_.edges(),
                            "Iniciamos el recorrido DFS para detectar componentes fuertemente conectados.");
}

void TarjanSolver::emit_trace_dfs_enter(int v) const {
    trace::emit_event_dfs_enter(++step_counter_, v, disc_[v], low_[v], stack_,
                                "Entramos al vértice y registramos su descubrimiento y low inicial.");
}

void TarjanSolver::emit_trace_edge(int u, int v, const std::string& kind, const std::string& caption) const {
    trace::emit_event_edge(++step_counter_, u, v, kind, caption);
}

void TarjanSolver::emit_trace_low_update(int v, int new_low, int via, const std::string& caption) const {
    trace::emit_event_low_update(++step_counter_, v, new_low, via, caption);
}

void TarjanSolver::emit_trace_dfs_exit(int v) const {
    trace::emit_event_dfs_exit(++step_counter_, v, disc_[v], low_[v],
                               "Termina la exploración de este vértice y se valida si ya forma un SCC.");
}

void TarjanSolver::emit_trace_scc_pop(const std::vector<int>& component, int scc_id) const {
    trace::emit_event_scc_pop(++step_counter_, component, scc_id,
                              "Se extrae un componente fuerte y se consolida como una unidad del grafo condensado.");
}

void TarjanSolver::emit_trace_end() const {
    trace::emit_event_end(++step_counter_, components_,
                          "El algoritmo finaliza y el grafo queda particionado en componentes fuertemente conexos.");
}
