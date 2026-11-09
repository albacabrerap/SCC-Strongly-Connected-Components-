from manim import *

from manim.common.theme import BACKGROUND, ACCENT, TEXT, MUTED


class S00Title(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        title = Text("SCC", font_size=90, color=ACCENT, weight='BOLD')
        subtitle = Text("Strongly Connected Components", font_size=40, color=TEXT)
        course = Text("CS2023 — Algoritmos y Estructuras de Datos", font_size=28, color=MUTED)
        members = Text("Integrantes: por definir", font_size=24, color=TEXT)
        year = Text("2026-2", font_size=24, color=MUTED)

        title.to_edge(UP, buff=1.2)
        subtitle.next_to(title, DOWN, buff=0.5)
        course.next_to(subtitle, DOWN, buff=0.6)
        members.next_to(course, DOWN, buff=0.6)
        year.next_to(members, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.5)
        self.play(Write(subtitle), run_time=1.2)
        self.play(Write(course), run_time=1.2)
        self.play(Write(members), run_time=1.2)
        self.play(Write(year), run_time=1.0)
        self.wait(1.5)
