"""Report agent and its internal knowledge-retrieval agent."""

import json
import re
from pathlib import Path
from typing import Any

from agents import Agent, function_tool

from app.core.config import settings


STOP_WORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "been",
        "being",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "employee",
        "employees",
        "for",
        "from",
        "how",
        "in",
        "is",
        "may",
        "of",
        "on",
        "or",
        "should",
        "that",
        "the",
        "their",
        "them",
        "these",
        "they",
        "this",
        "to",
        "what",
        "when",
        "where",
        "who",
        "why",
        "with",
        "would",
    }
)


def tokenize_search_text(text: str) -> set[str]:
    """Return unique lowercase search terms without punctuation or stop words."""
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOP_WORDS
    }


def load_prompt(prompt_path: Path) -> str:
    """Load an agent instruction prompt from a Markdown file."""
    return prompt_path.read_text(encoding="utf-8").strip()


def load_chunks() -> list[dict[str, Any]]:
    """Load saved chunks from the knowledge-base file."""
    chunks_path: Path = settings.CHUNKS_PATH
    if not chunks_path.exists():
        raise FileNotFoundError(
            f"Knowledge base has not been seeded: {chunks_path}"
        )

    with chunks_path.open(encoding="utf-8") as chunk_file:
        return [
            json.loads(line)
            for line in chunk_file
            if line.strip()
        ]


def search_knowledge_base(query: str, top_k: int = 2) -> str:
    """
    Search the saved knowledge base using simple keyword matching.
    Returns relevant text chunks without generating an answer.
    """
    chunks = load_chunks()
    query_terms = tokenize_search_text(query)
    scored_chunks = []

    for chunk in chunks:
        chunk_text = str(chunk.get("text", ""))
        chunk_terms = tokenize_search_text(chunk_text)
        score = len(query_terms & chunk_terms)

        if score > 0:
            scored_chunks.append((score, chunk_text))

    scored_chunks.sort(reverse=True, key=lambda item: item[0])
    results = [text for _, text in scored_chunks[:top_k]]

    if not results:
        return "No relevant information was found in the knowledge base."

    return "\n\n".join(results)


@function_tool
def retrieve_information(query: str) -> str:
    """Search the saved knowledge-base chunks for relevant information."""
    return search_knowledge_base(query)


data_retriever = Agent(
    name="Data Retriever",
    model=settings.MODEL_NAME,
    instructions=load_prompt(settings.RETRIEVER_PROMPT),
    tools=[retrieve_information],
)


report_generator = Agent(
    name="Report Generator",
    model=settings.MODEL_NAME,
    instructions=load_prompt(settings.REPORT_GENERATOR),
    tools=[
        data_retriever.as_tool(
            tool_name="retrieve_from_knowledge_base",
            tool_description="Retrieve relevant saved knowledge-base chunks.",
        )
    ],
)
