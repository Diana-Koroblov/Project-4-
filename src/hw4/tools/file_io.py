"""Tool: sandboxed read/write of source files.

Both operations are confined to the ``src/broken-python/`` subtree. Any path
that resolves outside that tree — including via ``..`` traversal — is rejected
with ``PermissionError``. This is the only sanctioned way for a subagent to
mutate vendored source, guaranteeing it cannot touch the orchestration code or
anything else in the repository.
"""

from pathlib import Path

from hw4.constants import ALLOWED_SOURCE_ROOT

_ALLOWED_ROOT = Path(ALLOWED_SOURCE_ROOT).resolve()


def _resolve_within_sandbox(path: str) -> Path:
    """Resolve ``path`` and confirm it falls inside the allowed source root.

    Raises:
        ValueError: If ``path`` is empty.
        PermissionError: If the resolved path escapes ``src/broken-python/``.
    """
    if not path or not str(path).strip():
        raise ValueError("path must be a non-empty string")

    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    resolved = candidate.resolve()

    if resolved != _ALLOWED_ROOT and not resolved.is_relative_to(_ALLOWED_ROOT):
        raise PermissionError(
            f"Path {path!r} is outside the allowed source root {ALLOWED_SOURCE_ROOT!r}"
        )
    return resolved


def read_source_file(path: str) -> str:
    """Return the UTF-8 contents of a file inside ``src/broken-python/``.

    Raises:
        PermissionError: If ``path`` resolves outside the allowed root.
        FileNotFoundError: If the file does not exist.
    """
    resolved = _resolve_within_sandbox(path)
    if not resolved.is_file():
        raise FileNotFoundError(f"Source file not found: {path}")
    return resolved.read_text(encoding="utf-8")


def write_source_file(path: str, content: str) -> None:
    """Write ``content`` to a file inside ``src/broken-python/``.

    Parent directories within the sandbox are created as needed.

    Raises:
        PermissionError: If ``path`` resolves outside the allowed root.
    """
    resolved = _resolve_within_sandbox(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(content, encoding="utf-8")
