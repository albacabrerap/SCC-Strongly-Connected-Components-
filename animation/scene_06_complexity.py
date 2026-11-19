import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *


class S06Complexity(Scene):
    def construct(self):
        title = Text("Análisis de complejidad", font_size=40, color=BLUE_B).to_edge(UP)
        self.play(Write(title))

        xs = (-6.5, 1.6, 4.0)
        header = VGroup(*[
            Text(t, font_size=24, weight=BOLD, color=YELLOW).move_to(RIGHT * x + UP * 2.0, aligned_edge=LEFT)
            for t, x in zip(("Operación elemental", "Costo", "Veces"), xs)
        ])
        line = Line(LEFT * 6.5 + UP * 1.65, RIGHT * 6.5 + UP * 1.65, color=GRAY_B)
        self.play(FadeIn(header), Create(line))

        rows = [
            ("Visitar vértice (disc, low, push)", "O(1)", "V"),
            ("Examinar una arista", "O(1)", "E"),
            ("Actualizar low[v]", "O(1)", "≤ E"),
            ("Desapilar vértice (unstack)", "O(1)", "V"),
        ]
        for i, row in enumerate(rows):
            y = 1.2 - i * 0.6
            cells = VGroup(*[Text(c, font_size=24).move_to(RIGHT * x + UP * y, aligned_edge=LEFT)
                             for c, x in zip(row, xs)])
            self.play(FadeIn(cells, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.6)

        total = Text("Total:  V·O(1) + E·O(1)  =  O(V + E)", font_size=34, color=GREEN_C).move_to(DOWN * 1.5)
        self.play(Write(total))
        self.wait(1.5)

        notes = VGroup(
            Text("Memoria: O(V)  (disc, low, onStack, pila y recursión del DFS)", font_size=22),
            Text("Kosaraju: también O(V + E), pero con 2 DFS y el grafo transpuesto", font_size=22, color=GRAY_A),
            Text("Después de preprocesar: ¿u y v en la misma SCC? → O(1) con un arreglo comp[ ]",
                 font_size=22, color=GRAY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(total, DOWN, buff=0.4)
        for note in notes:
            self.play(FadeIn(note, shift=UP * 0.15), run_time=0.6)
            self.wait(1.2)
        self.wait(1.5)
        self.play(FadeOut(*self.mobjects))