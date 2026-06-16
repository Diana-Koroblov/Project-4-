from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage

from hw4.constants import OBSIDIAN_POLYGONS_PAGE
from hw4.state import AgentState

_SYSTEM_PROMPT = (
    "You are Subagent Alpha, a specialist in the Polygons domain. "
    f"Begin your investigation from the Obsidian page: {OBSIDIAN_POLYGONS_PAGE}. "
    "Your scope is strictly limited to the Polygons community."
)


def make_alpha_node(llm: BaseChatModel):
    """Return the SubagentAlpha node bound to the given LLM (stub for Phase 4)."""
    def subagent_alpha_node(state: AgentState) -> dict:
        response = llm.invoke([SystemMessage(content=_SYSTEM_PROMPT)])
        return {
            "messages": [response],
            "completed_tasks": state["completed_tasks"] + ["alpha:polygons:complete"],
        }
    return subagent_alpha_node
