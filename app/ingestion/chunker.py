"""
Text chunking utilities for RAG document processing.
Implements simple word-based chunking with overlap for optimal retrieval.
"""

import logging
import re
from typing import Any, Dict, List, Optional

from app.core.config import settings


logger = logging.getLogger(__name__)


class TextChunker:
    """Simple text chunker with word-based splitting and overlap."""

    def __init__(
        self,
        chunk_size: Optional[int] = None,
        overlap: Optional[int] = None,
    ):
        """
        Initialize chunker with configuration.

        Args:
            chunk_size: Approximate tokens per chunk (default from settings)
            overlap: Overlap tokens between chunks (default from settings)
        """
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.overlap = overlap or settings.CHUNK_OVERLAP

        # Rough approximation: 1 token is about 0.75 words.
        self.words_per_chunk = int(self.chunk_size * 0.75)
        self.overlap_words = int(self.overlap * 0.75)

        logger.info(
            "Initialized chunker: ~%s words per chunk, %s overlap",
            self.words_per_chunk,
            self.overlap_words,
        )

    def chunk_text(
        self,
        text: str,
        source: str,
        base_chunk_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk
            source: Source identifier (URL, filename, etc.)
            base_chunk_id: Base identifier for generated chunks

        Returns:
            List of chunk dictionaries with chunk_id, source, and text
        """
        if not text or not text.strip():
            return []

        cleaned_text = self._clean_text(text)
        words = cleaned_text.split()

        if len(words) <= self.words_per_chunk:
            return [
                {
                    "chunk_id": f"{base_chunk_id}#1",
                    "source": source,
                    "text": cleaned_text,
                }
            ]

        chunks = []
        start_idx = 0
        chunk_num = 1

        while start_idx < len(words):
            end_idx = min(start_idx + self.words_per_chunk, len(words))
            chunk_text = " ".join(words[start_idx:end_idx])
            chunks.append(
                {
                    "chunk_id": f"{base_chunk_id}#{chunk_num}",
                    "source": source,
                    "text": chunk_text,
                }
            )

            if end_idx >= len(words):
                break

            start_idx = end_idx - self.overlap_words
            chunk_num += 1

        logger.info("Chunked text into %s chunks (source: %s)", len(chunks), source)
        return chunks

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize text before chunking."""
        text = re.sub(r"\s+", " ", text).strip()
        text = text.replace("“", '"').replace("”", '"')
        return text.replace("‘", "'").replace("’", "'")

    def chunk_documents(
        self,
        documents: List[Dict[str, str]],
    ) -> List[Dict[str, Any]]:
        """Chunk multiple documents."""
        all_chunks = []

        for document in documents:
            chunks = self.chunk_text(
                text=document.get("text", ""),
                source=document.get("source", "unknown"),
                base_chunk_id=document.get("chunk_id", "document"),
            )
            all_chunks.extend(chunks)

        logger.info(
            "Processed %s documents into %s chunks",
            len(documents),
            len(all_chunks),
        )
        return all_chunks


chunker = TextChunker()
