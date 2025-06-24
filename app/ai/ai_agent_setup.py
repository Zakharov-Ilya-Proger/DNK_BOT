from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider
from pydantic_ai.settings import ModelSettings

from app.db.db import get_data_from_db
from settings import settings

provider = DeepSeekProvider(
    api_key=settings.AI_API_KEY,
)

model = OpenAIModel(
    model_name="gpt-4.1",
    provider=provider,
)
agent = Agent(
    model=model,
    model_settings=ModelSettings(
        temperature=0.7,
    ),
    system_prompt=(
    )
)

@dataclass
class SupportedDeps:
    user_id: int

@agent.tool()
async def user_chat_history(ctx: RunContext[SupportedDeps]):
    dialog_history = await get_data_from_db(user_id=ctx.deps.user_id)
    return dialog_history

@agent.system_prompt()
async def information_to_answer():
    with open('app/text_to_answer.txt', 'r') as file:
        return file.read()
