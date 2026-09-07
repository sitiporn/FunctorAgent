"""API request models."""

from typing import List, Optional
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Request for an answer from the report agent."""
    query: str = Field(..., min_length=1, description="User's question")


class DocumentChunk(BaseModel):
    """Individual document chunk for seeding the knowledge base."""
    chunk_id: str = Field(..., description="Unique identifier for the chunk")
    source: str = Field(..., description="Source URL or identifier")
    text: str = Field(..., description="Text content of the chunk")
