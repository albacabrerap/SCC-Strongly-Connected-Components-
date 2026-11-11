from manim import *


class S00Title(Scene):
    def construct(self):
        title = Text("Tarjan y las SCC", font_size=54, weight=BOLD)
        subtitle = Text("Componentes fuertemente conexas", font_size=28, color=TEAL_A)
        course = Text("CS2023", font_size=24, color=YELLOW_A)
        names = Text(" Integrantes .d fdfd", font_size=26)

        title.shift(UP * 1.15)
        subtitle.next_to(title, DOWN, buff=0.25)
        course.shift(DOWN * 1.25)
        names.next_to(course, DOWN, buff=0.25)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(course), FadeIn(names, shift=UP * 0.15), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(VGroup(title, subtitle, course, names)), run_time=0.7)
