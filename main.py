"""Command-line entry point for the report agent."""

import argparse
import asyncio

from app.ingestion.document_ingestion import ensure_default_chunks
from app.services.agent_service import agent_service


def parse_args() -> argparse.Namespace:
    """Parse an optional question from the command line."""
    parser = argparse.ArgumentParser(description="Ask the report agent a question.")
    parser.add_argument(
        "query",
        nargs="*",
        help="Question for the agent; prompts interactively when omitted.",
    )
    return parser.parse_args()


async def main() -> None:
    """Prepare document chunks and run the report agent."""
    args = parse_args()
    query = " ".join(args.query).strip()
    if not query:
        query = input("Question: ").strip()
    if not query:
        raise ValueError("A question is required.")

    ensure_default_chunks()
    answer = await agent_service.generate_answer(query)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
