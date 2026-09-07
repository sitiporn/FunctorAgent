"""AI client configuration and report-agent execution."""

import logging

from agents import Runner, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI

from app.agents.report_generator import report_generator
from app.core.config import settings


logger = logging.getLogger(__name__)


class AgentService:
    """Configure the AI client and generate answers with the report agent."""

    def __init__(self) -> None:
        if settings.PROVIDER != "openai":
            raise ValueError(f"Unsupported AI provider: {settings.PROVIDER}")

        client = AsyncOpenAI(
            base_url=settings.API_BASE_URL,
            api_key="not-used",
            default_headers={"api-key": settings.APIM_API_KEY},
        )
        set_default_openai_client(client, use_for_tracing=False)
        set_tracing_disabled(True)

    async def generate_answer(self, query: str) -> str:
        """Run the report agent for a user query."""
        result = await Runner.run(report_generator, query)
        answer = str(result.final_output).strip()
        logger.info("Generated answer with %s", settings.MODEL_NAME)
        return answer or "I couldn't generate an answer."


agent_service = AgentService()
