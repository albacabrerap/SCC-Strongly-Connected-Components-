"""Helpers para leer la traza JSON generada por algorithm/tarjan."""
import json
from pathlib import Path


def load_trace(path="output/traza.json"):
    """
    Lee la traza y devuelve un dict con:
      - n: int
      - edges: list[tuple[int,int]]
      - events: list[dict]  (incluye el start y el finish)
    """
    raw = Path(path).read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in raw if line.strip()]
    start = next(e for e in events if e["event"] == "start")
    return {
        "n": start["n"],
        "edges": [tuple(e) for e in start["edges"]],
        "events": events,
    }