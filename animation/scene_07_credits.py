import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *
from utils.team import TITLE, COURSE, TEAM, REPO_URL


class S07Credits(Scene):
    def construct(self):
        head = Text("¡Gracias!", font_size=48, weight=BOLD, color=TEAL_A)
        refs = VGroup(
            Text("Referencias", font_size=22, weight=BOLD, color=GRAY_A),
            Text("R. Tarjan (1972). Depth-first search and linear graph algorithms. SIAM J. Comput. 1(2), 146–160.",
                 font_size=18, color=GRAY_A),
            Text("Manim Community Edition — docs.manim.community", font_size=18, color=GRAY_A),
            Text("Estilo inspirado en 3Blue1Brown", font_size=18, color=GRAY_A),
            Text(f"Código: {REPO_URL}", font_size=18, color=GRAY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if refs.width > 12.5:
            refs.scale_to_fit_width(12.5)
        VGroup(head, refs).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(Write(head))
        self.play(FadeIn(refs))
        self.wait(4)
        self.play(FadeOut(*self.mobjects))