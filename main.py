import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

# Re-exported so existing imports (`from main import build_graph`) keep working;
# the assembly itself now lives in the package and is exposed via the SDK.
from hw4.graph import build_graph
from hw4.sdk import GraphifySDK

__all__ = ["build_graph", "main"]


def main():
    """Print the compiled graph's Mermaid diagram (delegates to the SDK)."""
    print(GraphifySDK().graph_diagram())


if __name__ == "__main__":
    main()
