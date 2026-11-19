"""Reproduce una traza de Tarjan sobre grafo + tabla + pila."""
from manim import *
from utils.graph import DirectedGraph
from utils.components import StatusTable, StackPanel

SCC_COLORS = [GREEN_C, ORANGE, BLUE_C, RED_C, GOLD, PURPLE_C]


class TarjanPlayer:
    def __init__(self, scene, trace, positions, table_cols=(1.9, 3.0, 4.1),
                 stack_x=6.0, node_radius=0.32):
        self.scene, self.trace = scene, trace
        n = trace["n"]
        self.graph = DirectedGraph(
            vertices=list(range(n)), edges=trace["edges"], positions=positions,
            node_color=TEAL_A, edge_color=GRAY_B, fill_opacity=0.15, node_radius=node_radius,
        )
        self.table = StatusTable(n, x_cols=table_cols)
        self.stack = StackPanel(n, x=stack_x)
        self.msg = Text("Iniciando Tarjan...", font_size=24, color=YELLOW).to_edge(DOWN, buff=0.4)

    def circle(self, v):
        return self.graph.vertices_dict[v][0]

    def say(self, text, color=WHITE):
        new = Text(text, font_size=24, color=color).to_edge(DOWN, buff=0.4)
        if new.width > 12.5:
            new.scale_to_fit_width(12.5)
        anim = ReplacementTransform(self.msg, new)
        self.msg = new
        return anim

    def intro(self, rt=1.5):
        self.scene.play(Create(self.graph), FadeIn(self.table), FadeIn(self.stack),
                        FadeIn(self.msg), run_time=rt)

    def run(self, rt=0.6, hold=0.4):
        sc, ev = self.scene, self.trace["events"]
        comp = 0
        for i, e in enumerate(ev):
            k = e["event"]
            prev = ev[i - 1] if i else None

            if k == "enter":
                v = e["v"]
                od, nd = self.table.set_disc(v, e["disc"])
                ol, nl = self.table.set_low(v, e["low"])
                sc.play(self.circle(v).animate.set_fill(YELLOW_E, opacity=0.8),
                        Transform(od, nd), Transform(ol, nl),
                        self.say(f"Visitamos {v}: disc[{v}] = low[{v}] = {e['disc']}", YELLOW_A),
                        run_time=rt)

            elif k == "push":
                item = self.stack.push_anim(e["v"])
                sc.play(FadeIn(item, shift=DOWN * 0.4),
                        self.say(f"Apilamos {e['v']}", TEAL_A), run_time=rt)

            elif k == "edge":
                u, v, t = e["u"], e["v"], e["type"]
                mob = self.graph.edges_dict.get((u, v))
                if t == "tree":
                    col, txt = TEAL_A, f"Arista {u}→{v}: {v} sin visitar, bajamos con DFS"
                else:
                    col, txt = ORANGE, f"Arista {u}→{v}: {v} sigue en la pila (retroceso)"
                anims = [self.say(txt, col)]
                if mob is not None:
                    anims.append(mob.animate.set_color(col))
                sc.play(*anims, run_time=rt)

            elif k == "low_update":
                v, l = e["v"], e["low"]
                ol, nl = self.table.set_low(v, l, color=ORANGE)
                if prev and prev["event"] == "edge" and prev["type"] == "back" and prev["u"] == v:
                    why = f"low[{v}] = min(low[{v}], disc[{prev['v']}]) = {l}"
                else:
                    why = f"Volvemos a {v}: low[{v}] = min(low[{v}], low[hijo]) = {l}"
                sc.play(Transform(ol, nl), self.say(why, ORANGE), run_time=rt)

            elif k == "unstack":
                v = e["v"]
                if not (prev and prev["event"] == "unstack"):
                    j = i
                    while ev[j]["event"] == "unstack":
                        j += 1
                    root = ev[j - 1]["v"]
                    txt = f"low[{root}] = disc[{root}] → {root} es raíz de SCC. Desapilamos hasta {root}"
                else:
                    txt = f"Desapilamos {v}"
                item = self.stack.pop_anim()
                sc.play(FadeOut(item, shift=RIGHT * 0.6), self.say(txt, RED_B), run_time=rt)

            elif k == "pop":
                col = SCC_COLORS[comp % len(SCC_COLORS)]
                comp += 1
                scc = e["scc"]
                sc.play(*[self.circle(v).animate.set_fill(col, opacity=0.9) for v in scc],
                        self.say("¡SCC encontrada! {" + ", ".join(map(str, scc)) + "}", col),
                        run_time=rt + 0.2)
                sc.wait(hold)

            elif k == "finish":
                sc.play(self.say(f"Fin: {e['scc_count']} componentes fuertemente conexas", YELLOW),
                        run_time=rt)