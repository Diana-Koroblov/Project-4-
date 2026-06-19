"""hw4.sdk — Public SDK layer (§4.1).

:class:`GraphifySDK` is the sole entry point for all consumers (CLI, future GUI,
third-party integrations). Import it and run any operation without reaching into
internal modules:

    from hw4.sdk import GraphifySDK
    sdk = GraphifySDK()
    print(sdk.graph_diagram())     # compiled graph as Mermaid
    result = sdk.run_repair()      # full multi-agent repair run
    stats = sdk.compare_efficiency()
    orphans = sdk.detect_orphans()
"""

from hw4.sdk.core import GraphifySDK
from hw4.sdk.repair import DEFAULT_SEED, RepairResult
from hw4.shared.version import VERSION as __version__

__all__ = ["DEFAULT_SEED", "GraphifySDK", "RepairResult", "__version__"]
