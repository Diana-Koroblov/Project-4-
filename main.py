import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from langgraph.graph import END, START, StateGraph

from hw4.agents.alpha import make_alpha_node
from hw4.agents.beta import make_beta_node
from hw4.llm_config import get_llm
from hw4.nodes.gatekeeper import gatekeeper_node
from hw4.nodes.router import router_node
from hw4.state import AgentState


def build_graph(llm=None):
    """Compile and return the sequential StateGraph.

    Accepts an optional llm override (used in tests to inject a fake model).
    """
    if llm is None:
        llm = get_llm()

    graph = StateGraph(AgentState)
    graph.add_node("Router", router_node)
    graph.add_node("SubagentAlpha", make_alpha_node(llm))
    graph.add_node("Gatekeeper", gatekeeper_node)
    graph.add_node("SubagentBeta", make_beta_node(llm))

    graph.add_edge(START, "Router")
    graph.add_edge("Router", "SubagentAlpha")
    graph.add_edge("SubagentAlpha", "Gatekeeper")
    graph.add_edge("Gatekeeper", "SubagentBeta")
    graph.add_edge("SubagentBeta", END)

    return graph.compile()


def main():
    app = build_graph()
    print(app.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
