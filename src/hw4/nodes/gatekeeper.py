from langchain_core.messages import RemoveMessage

from hw4.constants import PHASE_MATHSQUIZ, PHASE_POLYGONS_COMPLETE_MARKER
from hw4.state import AgentState


def gatekeeper_node(state: AgentState) -> dict:
    """Gatekeeper: logs Alpha completions, purges messages, advances to mathsquiz phase."""
    clear_messages = [RemoveMessage(id=m.id) for m in state["messages"] if m.id]
    updated_tasks = list(state["completed_tasks"]) + [PHASE_POLYGONS_COMPLETE_MARKER]

    return {
        "current_phase": PHASE_MATHSQUIZ,
        "messages": clear_messages,
        "completed_tasks": updated_tasks,
    }
