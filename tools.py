
from datetime import datetime
from pathlib import Path

import wikipedia

from langchain_core.tools import Tool
from langchain_community.tools import (
    WikipediaQueryRun,
    DuckDuckGoSearchRun,
)
from langchain_community.utilities import WikipediaAPIWrapper


# Configure Wikipedia requests
wikipedia.set_user_agent(
    "AIResearchAssistant/1.0 (Python research project)"
)


# -----------------------------------
# 1. Save research to a text file
# -----------------------------------
def save_to_txt(
    data: str,
    filename: str = "research_output.txt",
) -> str:
    """Save research results to a timestamped text file."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    formatted_text = (
        "\n--- Research Output ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"{data}\n\n"
    )

    filepath = Path(__file__).parent / filename

    with filepath.open("a", encoding="utf-8") as file:
        file.write(formatted_text)

    return f"Research successfully saved to {filepath}"


save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Save research findings to a text file.",
)


# -----------------------------------
# 2. DuckDuckGo web search
# -----------------------------------
search = DuckDuckGoSearchRun()


def safe_search(query: str) -> str:
    """Search the web and handle temporary errors."""

    try:
        return search.run(query)
    except Exception as error:
        return f"Web search temporarily failed: {error}"


search_tool = Tool(
    name="search",
    func=safe_search,
    description=(
        "Search the web for information about the user's topic. "
        "For current trends, technology, tourism, and applications, "
        "include the current year in the query when appropriate. "
        "Prefer recent sources and publication dates when available."
    ),
)


# -----------------------------------
# 3. Wikipedia search
# -----------------------------------
api_wrapper = WikipediaAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=2000,
)

# Create the original Wikipedia tool AFTER defining api_wrapper
wiki_tool_original = WikipediaQueryRun(
    api_wrapper=api_wrapper,
)


def safe_wikipedia_search(query: str) -> str:
    """Search Wikipedia and handle temporary network errors."""

    try:
        return wiki_tool_original.run(query)
    except Exception as error:
        return f"Wikipedia search temporarily failed: {error}"


wiki_tool = Tool(
    name="wikipedia",
    func=safe_wikipedia_search,
    description=(
        "Search Wikipedia for background information on the topic. "
        "If Wikipedia is unavailable, use other available sources."
    ),
)
