from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage

from hw4.constants import OBSIDIAN_MATHSQUIZ_PAGE
from hw4.state import AgentState
from hw4.tools.registry import bind_agent_tools

_SYSTEM_PROMPT = (
    "You are Subagent Beta, a specialist in the Math Quiz domain. "
    f"Begin your investigation from the Obsidian page: {OBSIDIAN_MATHSQUIZ_PAGE}. "
    "Your scope is strictly limited to the Math Quiz community."
)


def make_beta_node(llm: BaseChatModel):
    """Return the SubagentBeta node bound to the Math Quiz toolset (stub for Phase 5).

    Same tool-loop shape as Alpha: one turn over the running history, with the
    completion marker recorded only on the final, tool-free turn.
    """
    model = bind_agent_tools(llm)

    def subagent_beta_node(state: AgentState) -> dict:
        messages = [SystemMessage(content=_SYSTEM_PROMPT), *state["messages"]]
        response = model.invoke(messages)
        update: dict = {"messages": [response]}
        if not getattr(response, "tool_calls", None):
            update["completed_tasks"] = state["completed_tasks"] + ["beta:mathsquiz:complete"]
        return update

    return subagent_beta_node
