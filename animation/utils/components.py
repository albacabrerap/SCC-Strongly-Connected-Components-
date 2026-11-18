"""Componentes visuales reutilizables para las escenas de Tarjan."""
from manim import *


class StatusTable(VGroup):
    """Tabla V | disc | low. set_disc/set_low devuelven (old, new) para Transform(old, new)."""

    def __init__(self, n, x_cols=(-1.5, 0.0, 1.5), y_start=1.5, y_step=0.5,
                 title_text="Estado de Tarjan", **kwargs):
        super().__init__(**kwargs)
        self.n = n
        h_v = Text("V", font_size=28, weight=BOLD).move_to(RIGHT * x_cols[0] + UP * 2.2)
        h_disc = Text("disc", font_size=28, weight=BOLD).move_to(RIGHT * x_cols[1] + UP * 2.2)
        h_low = Text("low", font_size=28, weight=BOLD).move_to(RIGHT * x_cols[2] + UP * 2.2)
        title = Text(title_text, font_size=32, weight=BOLD)
        title.move_to((h_v.get_center() + h_low.get_center()) / 2 + UP * 0.8)
        self.add(title, h_v, h_disc, h_low)

        self.rows = {}
        for i in range(n):
            y = y_start - i * y_step
            cell_v = Text(str(i), font_size=24).move_to(RIGHT * x_cols[0] + UP * y)
            cell_d = Text("-", font_size=24).move_to(RIGHT * x_cols[1] + UP * y)
            cell_l = Text("-", font_size=24).move_to(RIGHT * x_cols[2] + UP * y)
            self.rows[i] = {"disc": cell_d, "low": cell_l}
            self.add(cell_v, cell_d, cell_l)

    def set_disc(self, v, value, color=WHITE):
        old = self.rows[v]["disc"]          # la celda en pantalla NO cambia de referencia
        new = Text(str(value), font_size=24, color=color).move_to(old)
        return old, new

    def set_low(self, v, value, color=WHITE):
        old = self.rows[v]["low"]
        new = Text(str(value), font_size=24, color=color).move_to(old)
        return old, new


class StackPanel(VGroup):
    """Pila vertical (el fondo abajo, el tope arriba). Los items NO son hijos del panel:
    se animan como mobjects sueltos (FadeIn al apilar, FadeOut al desapilar)."""

    def __init__(self, n, x=6.0, y_bottom=-2.2, slot_h=0.5, title_text="Pila", **kwargs):
        super().__init__(**kwargs)
        self.x, self.y_bottom, self.slot_h = x, y_bottom, slot_h
        self.items = []
        height = max(n, 1) * slot_h
        self.border = Rectangle(width=1.4, height=height, color=GRAY_B, stroke_width=2)
        self.border.move_to(RIGHT * x + UP * (y_bottom + height / 2))
        self.title = Text(title_text, font_size=28, weight=BOLD).next_to(self.border, UP, buff=0.25)
        self.add(self.title, self.border)

    def slot_y(self, idx):
        return self.y_bottom + (idx + 0.5) * self.slot_h

    def push_anim(self, v):
        box = RoundedRectangle(width=1.1, height=self.slot_h * 0.8, corner_radius=0.08,
                               color=TEAL_A, fill_color=TEAL_E, fill_opacity=0.35, stroke_width=2)
        item = VGroup(box, Text(str(v), font_size=22))
        item.move_to(RIGHT * self.x + UP * self.slot_y(len(self.items)))
        self.items.append(item)
        return item

    def pop_anim(self):
        return self.items.pop() if self.items else None