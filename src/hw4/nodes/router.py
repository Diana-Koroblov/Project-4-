from pathlib import Path

from hw4.constants import OBSIDIAN_INDEX_PAGE, PHASE_POLYGONS
from hw4.state import AgentState

_OBSIDIAN_DIR = Path("obsidian")


def router_node(state: AgentState) -> dict:
    """Master Router: reads the Obsidian index and seeds initial agent state."""
    index_path = _OBSIDIAN_DIR / f"{OBSIDIAN_INDEX_PAGE}.md"
    if not index_path.exists():
        raise FileNotFoundError(f"Obsidian index not found: {index_path}")

    index_content = index_path.read_text(encoding="utf-8")

    return {
        "current_phase": PHASE_POLYGONS,
        "errors": [],
        "completed_tasks": [],
        "token_log": [{"event": "router_loaded_index", "chars": len(index_content)}],
    }
