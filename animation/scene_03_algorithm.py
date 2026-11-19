import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *
from utils.trace import load_trace
from utils.layouts import MINI_POSITIONS
from utils.player import TarjanPlayer
from utils.captions import CaptionScene


class S03Algorithm(CaptionScene):
    def construct(self):
        title = Text("Algoritmo de Tarjan: la idea", font_size=40, color=BLUE_B).to_edge(UP)
        self.play(Write(title))
        sub = Text("Una sola pasada de DFS con 3 ingredientes:", font_size=28, color=GRAY_A)
        sub.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(sub))

        c1 = Text("1. disc[v]: orden en que el DFS descubre a v", font_size=26, color=TEAL_A)
        c2 = Text("2. low[v]: el menor disc al que v puede volver\n    (por su subárbol + una arista de retroceso)",
                  font_size=26, color=ORANGE)
        c3 = Text("3. Pila: vértices visitados cuya SCC aún no se cierra", font_size=26, color=BLUE_C)
        cards = VGroup(c1, c2, c3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(sub, DOWN, buff=0.5)
        for c in (c1, c2, c3):
            self.play(FadeIn(c, shift=RIGHT * 0.3))
            self.wait(1.5)

        rule = Text("low[v] = disc[v]   ⇒   v es la raíz de una SCC\n(desapilamos hasta v: esos vértices son la componente)",
                    font_size=26, color=YELLOW)
        rule.next_to(cards, DOWN, buff=0.6)
        box = SurroundingRectangle(rule, color=YELLOW, buff=0.2)
        self.play(Write(rule), Create(box))
        self.wait(3)
        self.play(FadeOut(sub, cards, rule, box))

        # ---- Pseudocódigo ----
        code = Text(
            "dfs(v):\n"
            "  disc[v] = low[v] = t++ ;  apilar(v)\n"
            "  para cada arista v → u:\n"
            "    si u sin visitar:\n"
            "      dfs(u)\n"
            "      low[v] = min(low[v], low[u])\n"
            "    sino si u está en la pila:\n"
            "      low[v] = min(low[v], disc[u])\n"
            "  si low[v] == disc[v]:\n"
            "    desapilar hasta v  →  nueva SCC",
            font="Monospace", font_size=22, line_spacing=1.1,
        ).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(code))
        self.wait(7)
        self.play(FadeOut(code))

        # ---- Mini ejemplo con traza real ----
        title2 = Text("Ejemplo pequeño (traza real del programa en C++)", font_size=28, color=BLUE_B).to_corner(UL, buff=0.4)
        self.play(ReplacementTransform(title, title2))
        trace = load_trace("output/traza_mini.json")
        player = TarjanPlayer(self, trace, MINI_POSITIONS, node_radius=0.4)
        player.intro()
        self.wait(0.5)
        player.run(rt=0.9, hold=0.6)
        self.wait(2)
        self.play(FadeOut(*self.mobjects))