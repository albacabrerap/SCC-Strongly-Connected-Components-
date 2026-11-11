import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from manim import *
from utils.graph import DirectedGraph

class S02Demo(Scene):
    def construct(self):
        trace_path = Path("output/traza.json")
        with trace_path.open(encoding="utf-8") as f:
            events = [json.loads(line) for line in f if line.strip()]

        start_event = next(e for e in events if e["event"] == "start")
        n = start_event["n"]
        edges = [tuple(e) for e in start_event["edges"]]

        # 1. Configurar Grafo (más a la izquierda para dar espacio a la tabla)
        positions = {
            0: (-4.5, 1.5), 1: (-2.5, 1.5), 2: (-3.5, 0),
            3: (-0.5, 0),
            4: (1.5, 1.5), 5: (3.5, 1.5), 6: (3.5, -0.5), 7: (1.5, -0.5)
        }
        graph = DirectedGraph(
            vertices=list(range(n)), edges=edges, positions=positions, 
            node_color=TEAL_A, edge_color=GRAY_B, fill_opacity=0.15
        )
        graph.scale(0.75).shift(LEFT * 2.5)

        # 2. Construir Tabla Matemáticamente Perfecta (Coordenadas Fijas)
        # Definimos dónde va el centro de cada columna
        x_col_v = -1.5
        x_col_disc = 0.0
        x_col_low = 1.5
        
        # Posición inicial Y para la primera fila, y cuánto bajar en cada iteración
        y_start = 1.5
        y_step = 0.5

        # Encabezados (con tamaño uniforme)
        h_v = Text("V", font_size=28, weight=BOLD).move_to(RIGHT * x_col_v + UP * 2.2)
        h_disc = Text("disc", font_size=28, weight=BOLD).move_to(RIGHT * x_col_disc + UP * 2.2)
        h_low = Text("low", font_size=28, weight=BOLD).move_to(RIGHT * x_col_low + UP * 2.2)
        
        table_title = Text("Estado de Tarjan", font_size=32, weight=BOLD).next_to(h_v, UP, buff=0.6)
        # Centrar el título con respecto a las 3 columnas
        table_title.move_to((h_v.get_center() + h_low.get_center()) / 2 + UP * 0.8)

        table_elements = VGroup(table_title, h_v, h_disc, h_low)
        rows = {}

        # Generar las celdas vacías de la tabla
        for i in range(n):
            y_pos = y_start - (i * y_step)
            
            cell_v = Text(str(i), font_size=24).move_to(RIGHT * x_col_v + UP * y_pos)
            cell_d = Text("-", font_size=24).move_to(RIGHT * x_col_disc + UP * y_pos)
            cell_l = Text("-", font_size=24).move_to(RIGHT * x_col_low + UP * y_pos)
            
            rows[i] = {"disc": cell_d, "low": cell_l}
            table_elements.add(cell_v, cell_d, cell_l)

        # Mover toda la tabla al lado derecho de la pantalla
        table_group = VGroup(table_elements).scale(0.85).to_edge(RIGHT, buff=1.0)
        self.add(table_group)

        # 3. Iniciar Animación
        intro = Text("Iniciando Tarjan...", font_size=28, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Create(graph), FadeIn(intro))
        self.wait(2)
        self.play(FadeOut(intro))

        scc_colors = [GREEN_C, ORANGE, BLUE_C, RED_C, GOLD]
        comp_index = 0
        status_text = Text("", font_size=24, color=GRAY_A).to_edge(DOWN, buff=0.5)

        for event in events:
            if event["event"] == "start": continue

            if event["event"] == "enter":
                v, d, l = event["v"], event["disc"], event["low"]
                
                # Actualizar solo las celdas correspondientes
                new_d = Text(str(d), font_size=24).move_to(rows[v]["disc"])
                new_l = Text(str(l), font_size=24).move_to(rows[v]["low"])
                
                msg = Text(f"Entramos al nodo {v}. disc={d}, low={l}", font_size=24, color=YELLOW_A).to_edge(DOWN, buff=0.5)
                self.play(
                    graph.vertices_dict[v][0].animate.set_fill(YELLOW_E, opacity=0.8),
                    Transform(rows[v]["disc"], new_d),
                    Transform(rows[v]["low"], new_l),
                    Transform(status_text, msg),
                    run_time=0.6
                )

            elif event["event"] == "edge":
                u, v = event["u"], event["v"]
                edge = graph.edges_dict.get((u, v))
                msg = Text(f"Arista {u} -> {v}", font_size=24, color=TEAL_A).to_edge(DOWN, buff=0.5)
                
                anims = [Transform(status_text, msg)]
                if edge: anims.append(edge.animate.set_color(TEAL_A))
                self.play(*anims, run_time=0.5)
                if edge: self.play(edge.animate.set_color(GRAY_B), run_time=0.2)

            elif event["event"] == "pop":
                scc = event["scc"]
                color = scc_colors[comp_index % len(scc_colors)]
                comp_index += 1
                
                msg = Text(f"¡SCC Encontrado!: {{{', '.join(map(str, scc))}}}", font_size=24, color=color).to_edge(DOWN, buff=0.5)
                self.play(
                    *[graph.vertices_dict[v][0].animate.set_fill(color, opacity=0.9) for v in scc],
                    Transform(status_text, msg),
                    run_time=0.8
                )
                self.wait(0.5)

        self.wait(2)