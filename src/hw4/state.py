from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    current_phase: str
    messages: Annotated[list[BaseMessage], add_messages]
    errors: list[str]
    completed_tasks: list[str]
    token_log: list[dict]
