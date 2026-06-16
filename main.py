import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from hw4.agents.alpha import make_alpha_node
from hw4.agents.beta import make_beta_node
from hw4.llm_config import get_llm
from hw4.nodes.gatekeeper import gatekeeper_node
from hw4.nodes.router import router_node
from hw4.state import AgentState
from hw4.tools.registry import AGENT_TOOLS


def _has_tool_calls(state: AgentState) -> bool:
    messages = state["messages"]
    return bool(messages) and bool(getattr(messages[-1], "tool_calls", None))


def _alpha_route(state: AgentState) -> str:
    """Loop through AlphaTools while Alpha is calling tools, else hand off to the Gatekeeper."""
    return "AlphaTools" if _has_tool_calls(state) else "Gatekeeper"


def _beta_route(state: AgentState) -> str:
    """Loop through BetaTools while Beta is calling tools, else finish."""
    return "BetaTools" if _has_tool_calls(state) else END


def build_graph(llm=None):
    """Compile and return the sequential StateGraph.

    Accepts an optional llm override (used in tests to inject a fake model).
    Each subagent runs a bounded tool loop: while it emits tool calls the graph
    routes to its ToolNode and back; otherwise it advances down the pipeline.
    """
    if llm is None:
        llm = get_llm()

    graph = StateGraph(AgentState)
    graph.add_node("Router", router_node)
    graph.add_node("SubagentAlpha", make_alpha_node(llm))
    graph.add_node("AlphaTools", ToolNode(AGENT_TOOLS))
    graph.add_node("Gatekeeper", gatekeeper_node)
    graph.add_node("SubagentBeta", make_beta_node(llm))
    graph.add_node("BetaTools", ToolNode(AGENT_TOOLS))

    graph.add_edge(START, "Router")
    graph.add_edge("Router", "SubagentAlpha")
    graph.add_conditional_edges(
        "SubagentAlpha", _alpha_route, {"AlphaTools": "AlphaTools", "Gatekeeper": "Gatekeeper"}
    )
    graph.add_edge("AlphaTools", "SubagentAlpha")
    graph.add_edge("Gatekeeper", "SubagentBeta")
    graph.add_conditional_edges(
        "SubagentBeta", _beta_route, {"BetaTools": "BetaTools", END: END}
    )
    graph.add_edge("BetaTools", "SubagentBeta")

    return graph.compile()


def main():
    app = build_graph()
    print(app.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
