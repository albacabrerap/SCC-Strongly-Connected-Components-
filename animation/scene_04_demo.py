import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *
from utils.trace import load_trace
from utils.layouts import DEMO_POSITIONS
from utils.player import TarjanPlayer


class S04Demo(Scene):
    def construct(self):
        trace = load_trace("output/traza.json")
        title = Text("Demostración: Tarjan paso a paso", font_size=30, color=BLUE_B).to_corner(UL, buff=0.4)
        legend = VGroup(
            Text("— arista de árbol", font_size=20, color=TEAL_A),
            Text("— arista de retroceso", font_size=20, color=ORANGE),
            Text("● en el DFS", font_size=20, color=YELLOW_E),
        ).arrange(RIGHT, buff=0.5).move_to(LEFT * 3.2 + DOWN * 2.4)

        player = TarjanPlayer(self, trace, DEMO_POSITIONS, node_radius=0.32)
        self.play(Write(title), FadeIn(legend))
        player.intro(rt=2)
        self.wait(1.5)
        player.run(rt=0.6, hold=0.5)
        self.wait(1)
        self.play(player.say("Observa: Tarjan entrega las SCC en orden topológico inverso", YELLOW))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))