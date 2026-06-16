"""LangChain tool wrappers + binding helpers for the subagents.

The plain functions in this package stay callable as-is (used directly by the
graph nodes and unit tests). Here we additionally expose them as LangChain
``StructuredTool`` objects so a tool-calling LLM can invoke them by name, and a
``ToolNode`` can execute the resulting calls inside the graph.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import StructuredTool

from hw4.tools.file_io import read_source_file, write_source_file
from hw4.tools.node_extractor import extract_node_content
from hw4.tools.obsidian_reader import read_obsidian_page

read_obsidian_page_tool = StructuredTool.from_function(read_obsidian_page)
extract_node_content_tool = StructuredTool.from_function(extract_node_content)
read_source_file_tool = StructuredTool.from_function(read_source_file)
write_source_file_tool = StructuredTool.from_function(write_source_file)

# The full surgical toolset available to both subagents. Domain isolation is
# enforced by the system prompt and the file_io sandbox, not by withholding
# tools — both communities use the same precise read/extract/write primitives.
AGENT_TOOLS = [
    read_obsidian_page_tool,
    extract_node_content_tool,
    read_source_file_tool,
    write_source_file_tool,
]


def bind_agent_tools(llm: BaseChatModel):
    """Bind ``AGENT_TOOLS`` to ``llm``, degrading gracefully for fakes.

    Real chat models (e.g. ``ChatGroq``) gain tool-calling. Test doubles that
    do not implement ``bind_tools`` are returned unchanged so dry-run graph
    tests still execute.
    """
    try:
        return llm.bind_tools(AGENT_TOOLS)
    except NotImplementedError:
        return llm
