from manim import *


class CaptionScene(Scene):
    """Scene con una línea de subtítulo inferior que se reemplaza suavemente."""
    _cap = None

    def say(self, txt, color=WHITE, size=26):
        new = Text(txt, font_size=size, color=color).to_edge(DOWN, buff=0.5)
        if new.width > 12.5:
            new.scale_to_fit_width(12.5)
        old, self._cap = self._cap, new
        return ReplacementTransform(old, new) if old is not None else FadeIn(new)

    def clear_all(self, rt=0.7):
        self.play(FadeOut(*self.mobjects), run_time=rt)
        self._cap = None