import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *
from utils.graph import DirectedGraph
from utils.captions import CaptionScene


class S01Motivation(CaptionScene):
    def construct(self):
        title = Text("Instaladores de paquetes", font_size=40, color=BLUE_B).to_edge(UP)
        self.play(Write(title))
        self.play(self.say("Cada flecha X → Y significa: «X necesita a Y»", GRAY_A))
        self.wait(1)

        # --- Caso sin ciclos ---
        chain = DirectedGraph(
            vertices=["A", "B", "C"], edges=[("A", "B"), ("B", "C")],
            layout="horizontal", layout_scale=2.8, node_radius=0.5,
            node_color=TEAL_A, edge_color=GRAY_B, fill_opacity=0.15,
        )
        self.wait(6)
        self.play(Create(chain))
        for v in ["C", "B", "A"]:
            self.play(chain.vertices_dict[v][0].animate.set_fill(GREEN_C, opacity=0.8), run_time=1)
        self.wait(4)

        # --- Aparece el ciclo ---
        back = chain.add_edge("C", "A", color=RED_C, path_arc=-PI / 2)
        self.play(*[Indicate(chain.vertices_dict[v], color=RED) for v in "ABC"], run_time=2)
        self.wait(3)
        self.play(FadeOut(chain), FadeOut(back))

        # --- Caso realista: varios grupos ---
        positions = {"A": (-5, 0.9), "B": (-3, 0.9), "C": (-4, -1.0),
                     "D": (-1, -1.0), "E": (1, -1.0), "F": (0, 0.9)}
        edges = [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"),
                 ("D", "E"), ("E", "F"), ("F", "D")]
        big = DirectedGraph(vertices=list(positions), edges=edges, positions=positions,
                            node_radius=0.45, node_color=TEAL_A, edge_color=GRAY_B, fill_opacity=0.15)

        big.shift(RIGHT * 2)
        self.play(Create(big))

        self.wait(4)

        g1, g2 = ["A", "B", "C"], ["D", "E", "F"]
        lab1 = Text("Grupo 1: se instala junto", font_size=22, color=GREEN_C).next_to(
            VGroup(*[big.vertices_dict[v] for v in ("A", "B")]), UP, buff=0.35)
        lab2 = Text("Grupo 2: se instala junto", font_size=22, color=ORANGE).next_to(
            big.vertices_dict["F"], UP, buff=0.35)
        self.play(
            *[big.vertices_dict[v][0].animate.set_fill(GREEN_C, opacity=0.8) for v in g1],
            *[big.vertices_dict[v][0].animate.set_fill(ORANGE, opacity=0.8) for v in g2],
            FadeIn(lab1), FadeIn(lab2),
            self.say("Grupos de paquetes que se alcanzan mutuamente", YELLOW),
        )
        self.wait(3)
        self.play(self.say("Objetivo: encontrar esos grupos (SCC) en tiempo lineal", YELLOW, 28))
        self.wait(2)
        usos = Text("También se usa en: compiladores · 2-SAT · redes sociales · la web",
                    font_size=22, color=GRAY_A).next_to(self._cap, UP, buff=0.3)
        self.play(FadeIn(usos))
        self.wait(3)
        self.clear_all()