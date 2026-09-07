"""API response models."""

from pydantic import BaseModel, Field


class SeedResponse(BaseModel):
    """Result of document ingestion."""

    chunks_written: int = Field(..., ge=0)


class AgentDebugInfo(BaseModel):
    """Request timing information."""

    latency_ms: int = Field(..., ge=0)


class AgentResponse(BaseModel):
    """Answer returned by the report agent."""

    text: str
    debug: AgentDebugInfo
