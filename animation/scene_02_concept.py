import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *
import numpy as np
from utils.graph import DirectedGraph
from utils.trace import load_trace
from utils.layouts import DEMO_POSITIONS
from utils.player import SCC_COLORS
from utils.captions import CaptionScene


class S02Concept(CaptionScene):
    def construct(self):
        trace = load_trace("output/traza.json")
        n, edges = trace["n"], trace["edges"]
        sccs = [e["scc"] for e in trace["events"] if e["event"] == "pop"]   # orden de salida de Tarjan
        comp = {v: k for k, grp in enumerate(sccs) for v in grp}

        # ---- 1. Definición ----
        title = Text("¿Qué es una componente fuertemente conexa?", font_size=38, color=BLUE_B).to_edge(UP)
        self.play(Write(title))
        d1 = Text("SCC = conjunto MÁXIMO de vértices de un grafo dirigido\ntal que para todo par u, v del conjunto:",
                  font_size=28, line_spacing=1.2)
        d2 = Text("u alcanza a v      y      v alcanza a u", font_size=34, color=GREEN_C)
        d3 = Text("«alcanza» = existe un camino dirigido.  «Máximo» = no se puede agregar otro vértice.",
                  font_size=22, color=GRAY_A)
        VGroup(d1, d2, d3).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        self.play(FadeIn(d1, shift=UP * 0.2))
        self.play(Write(d2))
        self.play(FadeIn(d3))
        self.wait(3)
        self.play(FadeOut(d1, d2, d3))

        # ---- 2. Ejemplo visual con el grafo de la demo ----
        g = DirectedGraph(vertices=list(range(n)), edges=edges, positions=DEMO_POSITIONS,
                          node_radius=0.32, node_color=TEAL_A, edge_color=GRAY_B, fill_opacity=0.15)
        g.scale(1.25).move_to(ORIGIN + DOWN * 0.2)
        self.play(Create(g), self.say("¿Qué vértices se alcanzan mutuamente?", GRAY_A))
        self.wait(1)

        cyc = [g.edges_dict[(0, 1)], g.edges_dict[(1, 2)], g.edges_dict[(2, 0)]]
        self.play(*[e.animate.set_color(YELLOW) for e in cyc],
                  self.say("0 → 1 → 2 → 0: desde cualquiera llegamos a los otros dos", YELLOW))
        self.wait(1.5)

        anims = []
        for k, grp in enumerate(sccs):
            col = SCC_COLORS[k % len(SCC_COLORS)]
            anims += [g.vertices_dict[v][0].animate.set_fill(col, opacity=0.8) for v in grp]
            anims += [g.edges_dict[(u, v)].animate.set_color(col)
                      for u, v in edges if comp[u] == k and comp[v] == k]
        txt = f"{len(sccs)} SCC: " + "  ".join("{" + ",".join(map(str, sorted(s))) + "}" for s in sccs)
        self.play(*anims, self.say(txt, YELLOW))
        self.wait(1.5)
        self.play(self.say("Un vértice solo (el 3) también es una SCC: se alcanza a sí mismo", GRAY_A))
        self.wait(2.5)

        # ---- 3. Condensación: cada SCC colapsa a un nodo ----
        R = 0.6
        centers = {k: np.mean([g.vertices_dict[v].get_center() for v in grp], axis=0)
                   for k, grp in enumerate(sccs)}
        name = {k: f"C{len(sccs) - k}" for k in range(len(sccs))}    # C1 → C2 → C3 (orden topológico)
        supers = {}
        for k in range(len(sccs)):
            col = SCC_COLORS[k % len(SCC_COLORS)]
            circ = Circle(radius=R, color=col, fill_color=col, fill_opacity=0.35, stroke_width=4)
            supers[k] = VGroup(circ, Text(name[k], font_size=30)).move_to(centers[k])

        collapse = [FadeOut(g.edges_group)]
        for k, grp in enumerate(sccs):
            collapse += [g.vertices_dict[v].animate.move_to(centers[k]).set_opacity(0) for v in grp]
            collapse.append(FadeIn(supers[k]))
        self.play(*collapse, self.say("Colapsamos cada SCC en un solo nodo...", WHITE), run_time=1.6)
        self.remove(g)

        arrows = []
        for a, b in sorted({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]}):
            d = centers[b] - centers[a]
            d = d / np.linalg.norm(d)
            arrows.append(Arrow(centers[a] + d * R, centers[b] - d * R, buff=0,
                                color=GRAY_B, stroke_width=5))
        self.play(*[Create(a) for a in arrows], self.say("...y obtenemos el grafo condensado: ¡siempre es un DAG!", YELLOW))
        self.wait(2.5)
        self.play(self.say("Si hubiera un ciclo entre componentes, se fusionarían en una sola SCC", GRAY_A))
        self.wait(2.5)
        self.play(self.say("Instalación: C3, luego C2, luego C1 (orden topológico inverso)", GREEN_C))
        self.wait(3)
        self.clear_all()