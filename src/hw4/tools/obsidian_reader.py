"""Tool: read a single Obsidian vault page by name.

Lets a subagent retrieve a focused "hot" page (e.g. ``hot_polygons``) without
ever touching unrelated files in the vault.
"""

from pathlib import Path

_OBSIDIAN_DIR = Path("obsidian")


def read_obsidian_page(page_name: str) -> str:
    """Resolve ``page_name`` to ``obsidian/{page_name}.md`` and return its content.

    Args:
        page_name: The page stem without extension (e.g. ``"hot_polygons"``).
            A trailing ``.md`` is tolerated and stripped.

    Returns:
        The full UTF-8 text of the page.

    Raises:
        ValueError: If ``page_name`` is empty or attempts path traversal.
        FileNotFoundError: If the resolved page does not exist in the vault.
    """
    if not page_name or not page_name.strip():
        raise ValueError("page_name must be a non-empty string")

    stem = page_name.strip()
    if stem.endswith(".md"):
        stem = stem[: -len(".md")]

    # Reject any path separators or traversal — pages live flat in the vault.
    if "/" in stem or "\\" in stem or stem in (".", ".."):
        raise ValueError(f"Invalid page name: {page_name!r}")

    page_path = _OBSIDIAN_DIR / f"{stem}.md"
    if not page_path.exists():
        raise FileNotFoundError(f"Obsidian page not found: {page_path}")

    return page_path.read_text(encoding="utf-8")
