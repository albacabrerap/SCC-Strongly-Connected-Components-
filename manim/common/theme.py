from manim import *

BACKGROUND = '#0f172a'
PANEL = '#111827'
ACCENT = '#5eead4'
TEXT = '#e2e8f0'
MUTED = '#94a3b8'
STACK = '#fbbf24'
ACTIVE = '#f97316'
CLOSED = '#34d399'
EDGE = '#cbd5e1'
NODE = '#7dd3fc'
ERROR = '#f87171'

SCC_COLORS = [
    '#f59e0b',
    '#22c55e',
    '#38bdf8',
    '#a78bfa',
    '#f472b6',
    '#fb7185',
    '#2dd4bf',
    '#facc15',
]


def node_color_for_index(index: int) -> str:
    return SCC_COLORS[index % len(SCC_COLORS)]
