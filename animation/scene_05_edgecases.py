import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *
from utils.graph import DirectedGraph
from utils.trace import load_trace
from utils.player import SCC_COLORS

CASES = [
    ("Caso 1: grafo vacío (n = 0)", "output/traza_empty.json",
     "Sin vértices no hay DFS: 0 componentes"),
    ("Caso 2: un solo vértice (n = 1)", "output/traza_single.json",
     "Un vértice aislado es su propia SCC"),
    ("Caso 3: DAG (sin ciclos)", "output/traza_dag.json",
     "Cada vértice es su propia SCC: n componentes"),
    ("Caso 4: grafo completo K4 (peor caso en aristas)", "output/traza_complete.json",
     "Todos se alcanzan entre sí: 1 sola SCC"),
]


def build_graph(trace):
    n, edges = trace["n"], trace["edges"]
    g = DirectedGraph(vertices=list(range(n)), edges=[], layout="circular", layout_scale=1.8,
                      node_radius=0.4, node_color=TEAL_A, edge_color=GRAY_B, fill_opacity=0.15)
    eset = set(edges)
    for u, v in edges:
        g.add_edge(u, v, path_arc=(PI / 7 if (v, u) in eset else None))
    return g


class S05EdgeCases(Scene):
    def construct(self):
        for title, path, caption in CASES:
            t = load_trace(path)
            head = Text(title, font_size=34, color=BLUE_B).to_edge(UP, buff=0.5)
            cap = Text(caption, font_size=26, color=YELLOW).to_edge(DOWN, buff=0.5)
            count = next(e["scc_count"] for e in t["events"] if e["event"] == "finish")
            self.play(FadeIn(head))

            if t["n"] > 0:
                g = build_graph(t)
                g.move_to(ORIGIN + UP * 0.1)
                self.play(Create(g), run_time=1.2)
                sccs = [e["scc"] for e in t["events"] if e["event"] == "pop"]
                for k, scc in enumerate(sccs):
                    col = SCC_COLORS[k % len(SCC_COLORS)]
                    self.play(*[g.vertices_dict[v][0].animate.set_fill(col, opacity=0.9) for v in scc],
                              run_time=0.5)
            else:
                g = Text("V = { }", font_size=64, color=GRAY_B)
                self.play(FadeIn(g))

            res = Text(f"scc_count = {count}", font_size=30, color=GREEN_C).move_to(DOWN * 2.75)
            self.play(FadeIn(res), FadeIn(cap))
            self.wait(2)
            self.play(FadeOut(*self.mobjects), run_time=0.5)