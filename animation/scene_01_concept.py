import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *

class S01Concept(Scene):
    def construct(self):
        # --- 1. Motivación (Dependencias) ---
        title = Text("Motivación: Dependencias", font_size=40, color=BLUE_B).to_edge(UP)
        self.play(Write(title))
        
        a = Text("A", font_size=36).move_to(LEFT * 2 + DOWN * 1)
        b = Text("B", font_size=36).move_to(RIGHT * 2 + DOWN * 1)
        c = Text("C", font_size=36).move_to(UP * 1.5)
        
        arrow_ab = Arrow(a.get_right(), b.get_left(), buff=0.2)
        arrow_bc = Arrow(b.get_top(), c.get_bottom(), buff=0.2)
        arrow_ca = Arrow(c.get_left(), a.get_top(), buff=0.2)
        
        dep_graph = VGroup(a, b, c, arrow_ab, arrow_bc, arrow_ca)
        self.play(Create(dep_graph))
        
        mot_text = Text("¿Cómo instalar paquetes con\ndependencias cruzadas?", font_size=28, color=YELLOW).next_to(dep_graph, DOWN, buff=0.8)
        self.play(Write(mot_text))
        self.wait(2)
        self.play(FadeOut(title, dep_graph, mot_text))

        # --- 2. Definición Textual ---
        title2 = Text("Componente Fuertemente Conexa (SCC)", font_size=38, color=BLUE_B).to_edge(UP)
        self.play(Write(title2))
        
        def_text = Text(
            "Es un subgrafo donde para cualquier\n"
            "par de nodos u, v:\n\n"
            "1. Hay un camino de u hacia v.\n"
            "2. Hay un camino de v hacia u.",
            font_size=28, line_spacing=1.2
        ).next_to(title2, DOWN, buff=0.6)
        
        self.play(FadeIn(def_text, shift=UP))
        self.wait(3)
        self.play(FadeOut(def_text))

        # --- 3. Explicación Visual (Grafo de 4 nodos) ---
        # Movemos el título arriba
        title2.to_edge(UP, buff=0.5)
        
        u = Text("u", font_size=36).move_to(LEFT * 3 + DOWN * 0.5)
        v = Text("v", font_size=36).move_to(RIGHT * 3 + DOWN * 0.5)
        w = Text("w", font_size=36).move_to(UP * 1.5) 
        z = Text("z", font_size=36).move_to(DOWN * 2.5) 
        
        self.play(FadeIn(u), FadeIn(v), FadeIn(w), FadeIn(z))

        path_uv = VGroup(
            Arrow(u.get_top(), w.get_left(), buff=0.1, color=GREEN),
            Arrow(w.get_right(), v.get_top(), buff=0.1, color=GREEN)
        )
        path_vu = VGroup(
            Arrow(v.get_bottom(), z.get_right(), buff=0.1, color=TEAL_A),
            Arrow(z.get_left(), u.get_bottom(), buff=0.1, color=TEAL_A)
        )
        
        def_text1 = Text("u alcanza a v (por arriba)", font_size=24, color=GREEN).next_to(path_uv, UP, buff=0.3)
        def_text2 = Text("v alcanza a u (por abajo)", font_size=24, color=TEAL_A).next_to(path_vu, DOWN, buff=0.3)
        
        self.play(Create(path_uv), Write(def_text1))
        self.wait(1)
        self.play(Create(path_vu), Write(def_text2))
        
        def_text3 = Text("¡Se alcanzan mutuamente! Son un mismo SCC.", font_size=24, color=YELLOW).to_edge(DOWN, buff=0.2)
        self.play(Write(def_text3))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))

        # --- 4. Algoritmos disponibles ---
        title3 = Text("Algoritmos para resolverlo", font_size=40, color=BLUE_B).to_edge(UP)
        self.play(Write(title3))
        
        k_title = Text("1. Kosaraju (O(V + E))", font_size=28, color=GREEN).shift(UP * 1.5)
        k_desc = Text("Hace 2 pasadas de DFS:\n- En el grafo original.\n- En el grafo transpuesto.", font_size=22, color=GRAY_A).next_to(k_title, DOWN)
        
        t_title = Text("2. Tarjan (O(V + E))", font_size=28, color=ORANGE).shift(DOWN * 0.8)
        t_desc = Text("Hace 1 sola pasada de DFS.\n- Usa los tiempos disc y low.\n- Usa una pila (stack).", font_size=22, color=GRAY_A).next_to(t_title, DOWN)
        
        self.play(Write(k_title), FadeIn(k_desc))
        self.wait(1)
        self.play(Write(t_title), FadeIn(t_desc))
        
        decided = Text("¡Usaremos Tarjan! Es más eficiente.", font_size=26, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(decided))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))