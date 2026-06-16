from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage

from hw4.agents.beta_prompt import BETA_SYSTEM_PROMPT
from hw4.state import AgentState
from hw4.tools.registry import bind_agent_tools


def make_beta_node(llm: BaseChatModel):
    model = bind_agent_tools(llm)

    def subagent_beta_node(state: AgentState) -> dict:
        messages = [SystemMessage(content=BETA_SYSTEM_PROMPT), *state["messages"]]
        response = model.invoke(messages)
        update: dict = {"messages": [response]}
        if not getattr(response, "tool_calls", None):
            update["completed_tasks"] = state["completed_tasks"] + ["beta:mathsquiz:complete"]
        return update

    return subagent_beta_node
