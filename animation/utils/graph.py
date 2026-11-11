from manim import *

class DirectedGraph(VGroup):

  def __init__(
      self,
      vertices=None,
      edges=None,
      positions=None,
      layout="horizontal",
      layout_scale=2.5,
      node_radius=0.4,
      node_color=YELLOW_E,
      fill_color=BLACK,
      fill_opacity=0.2,
      text_color=WHITE,
      edge_color=YELLOW_A,
      stroke_width=3,
      **kwargs,
  ):
    super().__init__(**kwargs)

    self.node_radius = node_radius
    self.node_color = node_color
    self.fill_color = fill_color
    self.fill_opacity = fill_opacity
    self.text_color = text_color
    self.edge_color = edge_color
    self.stroke_width = stroke_width
    self.layout_scale = layout_scale

    # map vertices, edges, and 3D coordinates
    self.vertices_dict = {}
    self.edges_dict = {}
    self.positions = {}

    self.edges_group = VGroup()
    self.nodes_group = VGroup()
    self.add(self.edges_group, self.nodes_group)

    vertices = vertices or []
    edges = edges or []

    if positions:
      self.positions = {
          v: np.array([*pos, 0]) if len(pos) == 2 else np.array(pos)
          for v, pos in positions.items()
      }
    else:
      self.positions = self._calculate_layout(vertices, layout, layout_scale)

    for v in vertices:
      self.add_vertex(v, position=self.positions.get(v, ORIGIN))

    for u, v in edges:
      self.add_edge(u, v)

  def _calculate_layout(self, vertices, layout, scale):
    positions = {}
    n = len(vertices)
    if n == 0:
      return positions

    if layout == "horizontal":
      start_x = -scale * (n - 1) / 2
      for i, v in enumerate(vertices):
        positions[v] = np.array([start_x + i * scale, 0, 0])
    elif layout == "vertical":
      start_y = -scale * (n - 1) / 2
      for i, v in enumerate(vertices):
        positions[v] = np.array([0, start_y + i * scale, 0])
    else:
      for v in vertices:
        positions[v] = ORIGIN
    return positions

  def _create_node_mobject(self, v_id, position):
    circle = Circle(
        radius=self.node_radius,
        color=self.node_color,
        fill_color=self.fill_color,
        fill_opacity=self.fill_opacity,
        stroke_width=self.stroke_width,
    )
    label = Text(str(v_id), color=self.text_color).scale(0.55)
    node = VGroup(circle, label).move_to(position)
    node.v_id = v_id
    return node

  def add_vertex(self, vertid, position=None):
    if vertid in self.vertices_dict:
      return self.vertices_dict[vertid]

    pos = (
        np.array([*position, 0])
        if position is not None and len(position) == 2
        else position
    )
    if pos is None:
      pos = ORIGIN

    self.positions[vertid] = np.array(pos, dtype=float)
    node_mob = self._create_node_mobject(vertid, self.positions[vertid])

    self.vertices_dict[vertid] = node_mob
    self.nodes_group.add(node_mob)
    return node_mob

  def add_edge(self, u, v, color=None, path_arc=None):
    if u not in self.vertices_dict or v not in self.vertices_dict:
      raise ValueError(f"Vertices '{u}' or '{v}' don't exist yet.")

    edge_key = (u, v)
    edge_color = color or self.edge_color
    pos_u = self.positions[u]
    pos_v = self.positions[v]

    if u == v:
      out_vec = pos_u / np.linalg.norm(pos_u) if np.any(pos_u) else UP
      out_angle = np.arctan2(out_vec[1], out_vec[0])

      delta = 0.5
      start_pt = pos_u + self.node_radius * np.array(
          [np.cos(out_angle - delta), np.sin(out_angle - delta), 0]
      )
      end_pt = pos_u + self.node_radius * np.array(
          [np.cos(out_angle + delta), np.sin(out_angle + delta), 0]
      )

      edge_mob = CurvedArrow(
          start_pt,
          end_pt,
          angle=-TAU * 0.75,
          color=edge_color,
          stroke_width=self.stroke_width,
      )

    else:
      vec = pos_v - pos_u
      dist = np.linalg.norm(vec)

      if dist == 0:
        unit_vec = RIGHT
      else:
        unit_vec = vec / dist

      start_pt = pos_u + unit_vec * self.node_radius
      end_pt = pos_v - unit_vec * self.node_radius

      if path_arc is not None or (v, u) in self.edges_dict:
        arc_angle = path_arc if path_arc is not None else PI / 5
        edge_mob = CurvedArrow(
            start_pt,
            end_pt,
            angle=arc_angle,
            color=edge_color,
            stroke_width=self.stroke_width,
        )
      else:
        edge_mob = Arrow(
            start_pt,
            end_pt,
            buff=0,
            color=edge_color,
            stroke_width=self.stroke_width,
            max_tip_length_to_length_ratio=0.2,
        )

    self.edges_dict[edge_key] = edge_mob
    self.edges_group.add(edge_mob)
    return edge_mob