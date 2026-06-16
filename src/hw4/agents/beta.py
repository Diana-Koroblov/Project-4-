from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage

from hw4.constants import OBSIDIAN_MATHSQUIZ_PAGE
from hw4.state import AgentState

_SYSTEM_PROMPT = (
    "You are Subagent Beta, a specialist in the Math Quiz domain. "
    f"Begin your investigation from the Obsidian page: {OBSIDIAN_MATHSQUIZ_PAGE}. "
    "Your scope is strictly limited to the Math Quiz community."
)


def make_beta_node(llm: BaseChatModel):
    """Return the SubagentBeta node bound to the given LLM (stub for Phase 5)."""
    def subagent_beta_node(state: AgentState) -> dict:
        response = llm.invoke([SystemMessage(content=_SYSTEM_PROMPT)])
        return {
            "messages": [response],
            "completed_tasks": state["completed_tasks"] + ["beta:mathsquiz:complete"],
        }
    return subagent_beta_node
