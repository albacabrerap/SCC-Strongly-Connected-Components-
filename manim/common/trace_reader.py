import json
from pathlib import Path
from typing import Any, List


def load_trace(path: str | Path) -> List[dict[str, Any]]:
    data: List[dict[str, Any]] = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        data.append(json.loads(line))
    return data
