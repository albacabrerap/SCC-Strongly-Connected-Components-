from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

from manim import *

from .theme import *


class GraphView:
    def __init__(self, n: int, edges: Iterable[Tuple[int, int]], positions: Optional[Dict[int, np.ndarray]] = None):
        self.n = n
        self.edges = list(edges)
        self.positions = positions or self._default_positions(n)
        self.node_items: Dict[int, Circle] = {}
        self.edge_items: Dict[Tuple[int, int], Line] = {}
        self.labels: Dict[int, MathTex] = {}
        self.highlighted_edge: Optional[Tuple[int, int]] = None
        self.closed_components: Dict[int, str] = {}
        self.current_stack: List[int] = []
        self.current_values: Dict[int, Tuple[int, int]] = {}

    def _default_positions(self, n: int) -> Dict[int, np.ndarray]:
        coords: Dict[int, np.ndarray] = {}
        radius = 3.2
        for idx in range(n):
            angle = 2 * np.pi * idx / max(1, n)
            coords[idx] = np.array([radius * np.cos(angle), radius * np.sin(angle), 0.0])
        return coords

    def build(self) -> VGroup:
        group = VGroup()
        for u, v in self.edges:
            line = Line(self.positions[u], self.positions[v], stroke_color=EDGE, stroke_width=2)
            self.edge_items[(u, v)] = line
            group.add(line)

        for node_id in range(self.n):
            node = Circle(radius=0.42, stroke_color=NODE, fill_color=NODE, fill_opacity=0.22, stroke_width=2)
            node.move_to(self.positions[node_id])
            label = MathTex(str(node_id), color=TEXT, font_size=28)
            label.move_to(self.positions[node_id])
            self.node_items[node_id] = node
            self.labels[node_id] = label
            group.add(node, label)

        return group

    def highlight_edge(self, u: int, v: int, color: str = ACTIVE):
        key = (u, v)
        if key in self.edge_items:
            self.edge_items[key].set_stroke(color, width=4)
            self.highlighted_edge = key

    def clear_edge_highlight(self):
        for (u, v), line in self.edge_items.items():
            line.set_stroke(EDGE, width=2)
        self.highlighted_edge = None

    def mark_stack(self, stack: Iterable[int]):
        self.current_stack = list(stack)
        for node_id, node in self.node_items.items():
            if node_id in self.current_stack:
                node.set_fill(STACK, opacity=0.65)
                node.set_stroke(STACK, width=3)
            else:
                node.set_fill(NODE, opacity=0.22)
                node.set_stroke(NODE, width=2)

    def set_node_values(self, values: Dict[int, Tuple[int, int]]):
        self.current_values = values

    def mark_component(self, component: Iterable[int], component_id: int):
        color = node_color_for_index(component_id)
        for node_id in component:
            self.node_items[node_id].set_fill(color, opacity=0.75)
            self.node_items[node_id].set_stroke(color, width=3)
            self.closed_components[node_id] = color

    def reset_component_colors(self):
        for node_id, node in self.node_items.items():
            if node_id not in self.closed_components:
                node.set_fill(NODE, opacity=0.22)
                node.set_stroke(NODE, width=2)

    def update_from_event(self, event: dict):
        kind = event.get('event')
        if kind == 'start':
            self.clear_edge_highlight()
            self.reset_component_colors()
        elif kind == 'edge':
            self.clear_edge_highlight()
            self.highlight_edge(int(event['u']), int(event['v']))
        elif kind == 'dfs_enter':
            self.mark_stack(event.get('stack', []))
        elif kind == 'scc_pop':
            nodes = event.get('nodes', [])
            component_id = int(event.get('scc_id', 0))
            self.mark_component(nodes, component_id)
        elif kind == 'end':
            self.clear_edge_highlight()
