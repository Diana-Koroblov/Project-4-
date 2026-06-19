"""GraphifySDK — the single public entry point for all business operations (§4.1).

External consumers import this facade and never reach into internal modules:

    from hw4.sdk import GraphifySDK
    sdk = GraphifySDK()
    print(sdk.graph_diagram())
    result = sdk.run_repair()
    stats = sdk.compare_efficiency()

Each method delegates to an internal module; no business logic lives in the CLI
or other consumer layers. Heavy/optional dependencies are imported lazily inside
methods so merely importing the SDK stays cheap.
"""

from __future__ import annotations

from typing import Any

from hw4.extensions.orphan_detector import (
    DEFAULT_GRAPH_PATH,
    DEFAULT_REPORT_PATH,
    OrphanDetector,
    OrphanNode,
)
from hw4.graph import build_graph
from hw4.sdk.repair import DEFAULT_SEED, RepairResult, run_repair


class GraphifySDK:
    """Facade over graph orchestration, efficiency research, and graph analysis."""

    def __init__(self, llm: Any | None = None) -> None:
        # Optional LLM override (tests inject a fake); None => provider-configured.
        self._llm = llm

    # -- LLM / graph -------------------------------------------------------
    def get_llm(self) -> Any:
        """Return the configured (gatekept) LLM, building it once on first use."""
        if self._llm is None:
            from hw4.llm_config import get_llm

            self._llm = get_llm()
        return self._llm

    def build_graph(self) -> Any:
        """Compile and return the multi-agent StateGraph."""
        return build_graph(self._llm)

    def graph_diagram(self) -> str:
        """Return the Mermaid diagram of the compiled graph."""
        return self.build_graph().get_graph().draw_mermaid()

    def run_repair(
        self,
        seed: str = DEFAULT_SEED,
        *,
        recursion_limit: int = 20,
        callbacks: list | None = None,
    ) -> RepairResult:
        """Run the full Router->Alpha->Gatekeeper->Beta repair; return its result."""
        app = self.build_graph()
        return run_repair(app, seed, recursion_limit=recursion_limit, callbacks=callbacks)

    # -- Efficiency research ----------------------------------------------
    def compare_efficiency(self, tracker: Any | None = None) -> dict:
        """Deterministic baseline-vs-guided token comparison."""
        from hw4.efficiency import compare

        return compare(tracker)

    def measure_live_efficiency(self, **kwargs: Any) -> Any:
        """Measure real Groq token usage for baseline vs guided contexts."""
        from hw4.live_efficiency import run

        return run(**kwargs)

    # -- Graph analysis extension -----------------------------------------
    def detect_orphans(
        self, graph_path: str = DEFAULT_GRAPH_PATH, threshold: int | None = None
    ) -> list[OrphanNode]:
        """Return graph nodes with <= threshold edges (config-driven default)."""
        return OrphanDetector(graph_path, threshold=threshold).detect()

    def report_orphans(
        self,
        graph_path: str = DEFAULT_GRAPH_PATH,
        out: str = DEFAULT_REPORT_PATH,
        threshold: int | None = None,
    ) -> int:
        """Write the orphan Markdown report; return the orphan count."""
        detector = OrphanDetector(graph_path, threshold=threshold)
        detector.report(out)
        return len(detector.detect())
