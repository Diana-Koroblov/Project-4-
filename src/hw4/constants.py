"""Project-wide constants.

All configuration values are loaded from config/setup.json at runtime.
This module defines only true constants that never change between environments.
"""

# Graph phases
PHASE_POLYGONS = "polygons"
PHASE_MATHSQUIZ = "mathsquiz"

# Gatekeeper marker written to completed_tasks
PHASE_POLYGONS_COMPLETE_MARKER = "phase:polygons:complete"

# Default config paths (relative to project root)
CONFIG_SETUP_PATH = "config/setup.json"
CONFIG_SETUP_EXAMPLE_PATH = "config/setup.example.json"  # committed fallback default
CONFIG_RATE_LIMITS_PATH = "config/rate_limits.json"
CONFIG_LOGGING_PATH = "config/logging_config.json"

# Obsidian vault paths
OBSIDIAN_INDEX_PAGE = "index"
OBSIDIAN_POLYGONS_PAGE = "hot_polygons"
OBSIDIAN_MATHSQUIZ_PAGE = "hot_mathsquiz"

# Allowed source subtree for file I/O tools
ALLOWED_SOURCE_ROOT = "src/broken-python"

# Token efficiency KPI threshold (fraction)
TOKEN_EFFICIENCY_TARGET = 0.70  # >70% reduction vs. naive baseline

# Orphan detector default (used only if config/setup*.json is unavailable)
DEFAULT_ORPHAN_THRESHOLD = 1
