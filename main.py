"""Command-line entry point for the report agent."""

import argparse
import asyncio

from app.ingestion.document_ingestion import ensure_default_chunks
from app.services.agent_service import agent_service


TEST_QUESTIONS = [
    "What approvals are required before booking international business travel?",
    "When is business-class airfare allowed for an international trip?",
    "How many annual leave days do employees receive, and when should they request leave?",
    "What are the requirements for working remotely?",
    "What should an employee do if a company laptop is lost or stolen?",
]


def parse_args() -> argparse.Namespace:
    """Parse an optional question from the command line."""
    parser = argparse.ArgumentParser(description="Ask the report agent a question.")
    parser.add_argument(
        "query",
        nargs="*",
        help="Question for the agent; prompts interactively when omitted.",
    )
    return parser.parse_args()


def select_question() -> str:
    """Display example questions and return the selected or custom question."""
    print("Example questions:")
    for index, question in enumerate(TEST_QUESTIONS, start=1):
        print(f"{index}. {question}")

    selection = input("Choose 1-5 or type your own question: ").strip()
    if selection.isdigit() and 1 <= int(selection) <= len(TEST_QUESTIONS):
        return TEST_QUESTIONS[int(selection) - 1]
    return selection


async def main() -> None:
    """Prepare document chunks and run the report agent."""
    args = parse_args()
    query = " ".join(args.query).strip()
    if not query:
        query = select_question()
    if not query:
        raise ValueError("A question is required.")

    ensure_default_chunks()
    answer = await agent_service.generate_answer(query)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
