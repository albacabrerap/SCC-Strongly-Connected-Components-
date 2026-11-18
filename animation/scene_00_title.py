import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *
from utils.team import TITLE, SUBTITLE, COURSE, TEAM


class S00Title(Scene):
    def construct(self):
        title = Text(TITLE, font_size=44, weight=BOLD)
        if title.width > 12:
            title.scale_to_fit_width(12)
        subtitle = Text(SUBTITLE, font_size=30, color=TEAL_A)
        course = Text(COURSE, font_size=22, color=YELLOW_A)
        names = VGroup(*[Text(n, font_size=26) for n in TEAM]).arrange(DOWN, buff=0.15)
        group = VGroup(title, subtitle, course, names).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(course), FadeIn(names, shift=UP * 0.15), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(group), run_time=0.7)