"""Create and persist searchable document chunks."""

import json
from pathlib import Path

from app.core.config import settings
from app.ingestion.chunker import TextChunker


def load_default_documents() -> list[dict[str, str]]:
    """Load the configured knowledge-base file as an input document."""
    source_path = settings.KB_PATH
    return [
        {
            "chunk_id": source_path.stem,
            "source": str(source_path),
            "text": source_path.read_text(encoding="utf-8"),
        }
    ]


def seed_documents(documents: list[dict[str, str]] | None = None) -> int:
    """Chunk documents and atomically write them to the configured JSONL file."""
    input_documents = documents or load_default_documents()
    chunker = TextChunker(settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
    chunks = chunker.chunk_documents(input_documents)

    output_path = settings.CHUNKS_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(f"{output_path.suffix}.tmp")

    with temporary_path.open("w", encoding="utf-8") as output_file:
        for chunk in chunks:
            output_file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    temporary_path.replace(output_path)
    return len(chunks)


def ensure_default_chunks() -> int:
    """Regenerate default chunks only when missing or older than their source."""
    source_path: Path = settings.KB_PATH
    output_path: Path = settings.CHUNKS_PATH

    if (
        not output_path.exists()
        or output_path.stat().st_mtime < source_path.stat().st_mtime
    ):
        return seed_documents()

    with output_path.open(encoding="utf-8") as chunk_file:
        return sum(1 for line in chunk_file if line.strip())


if __name__ == "__main__":
    chunks_written = seed_documents()
    print(f"Saved {chunks_written} chunks to {settings.CHUNKS_PATH}")
