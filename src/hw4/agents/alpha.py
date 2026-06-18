from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage

from hw4.agents.alpha_prompt import ALPHA_SYSTEM_PROMPT
from hw4.state import AgentState
from hw4.tools.registry import bind_agent_tools
from hw4.tools.tool_call_repair import invoke_with_repair


def make_alpha_node(llm: BaseChatModel):
    """Return the SubagentAlpha node bound to the Polygons toolset.

    Runs one LLM turn over the running message history with the isolation
    system prompt prepended. If the model requests tools the graph routes to
    the tool node and re-enters here; the completion marker is recorded only
    on the final, tool-free turn.
    """
    model = bind_agent_tools(llm)

    def subagent_alpha_node(state: AgentState) -> dict:
        messages = [SystemMessage(content=ALPHA_SYSTEM_PROMPT), *state["messages"]]
        response = invoke_with_repair(model, messages)
        update: dict = {"messages": [response]}
        if not getattr(response, "tool_calls", None):
            update["completed_tasks"] = state["completed_tasks"] + ["alpha:polygons:complete"]
        return update

    return subagent_alpha_node
