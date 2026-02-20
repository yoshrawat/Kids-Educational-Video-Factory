# infrastructure/llm/litellm_provider.py
import litellm
from domain.interfaces.llm_provider import LLMProvider
from shared.settings.config import config


class LiteLLMProvider(LLMProvider):

    async def generate(self, prompt: str) -> str:
        response = await litellm.acompletion(
            model=config.llm.model,
            messages=[{"role": "user", "content": prompt}],
        )

        return response["choices"][0]["message"]["content"]