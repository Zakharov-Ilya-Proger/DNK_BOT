import logging
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.deepseek import DeepSeekProvider
from pydantic_ai.providers.mistral import MistralProvider
from pydantic_ai.settings import ModelSettings

from app.db.db import get_data_from_db
from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provider = DeepSeekProvider(
    api_key=settings.AI_API_KEY,
)

model = OpenAIModel(
    model_name="deepseek-chat",
    provider=provider,
) if not settings.IS_TEST else MistralModel(
    model_name="mistral-small-latest",
    provider=MistralProvider(
        api_key=settings.AI_MISTRAL_API_KEY,
    ),
)
agent = Agent(
    model=model,
    model_settings=ModelSettings(
        temperature=0.7,
    ),
    system_prompt=(
        "Ты официальный помощник, отвечающий на вопросы на основе предоставленного файла процессов. "
        "Строго придерживайся регламента и информации из файла.\n\n"
        "**Инструкции:**\n"
        "1. Всегда сохраняй вежливый и профессиональный тон\n"
        "2. Для понимания контекста при необходимости используй tool `user_chat_history`\n"
        "3. Форматируй ответы используя MARKDOWN (*, _, `, -)\n"
        "4. Если информации в файле недостаточно - вежливо уведомь\n\n"
        "5. Использовать только описанное форматирование текста"
        "6. Удерживай человека в направленности беседы, отвечай только на вопросы по теме"
        "7. Возвращай человека в русло беседы, если он пытается говорить о чем-то отстраненном"
        "*Форматирование:*\n"
        "- -Курсив- для акцента\n"
        "- *Жирный* для заголовков\n"
        "- `код` для терминов\n"
        "- Списки через дефис\n\n"
        "Не упоминай файл явно, если пользователь не спрашивает об источнике."
        "*Запрещается*"
        "Использовать для обозначения заголовков '#', только '*', так же, запрещается использовать '**' для обозначения жирного текста"
        "Отвечать на вопросы человека не по теме"
        "Отвечать на провокационные вопросы"
        "Использовать '---', только '\\n'"
    )
)

@dataclass
class SupportedDeps:
    user_id: int

@agent.tool()
async def user_chat_history(ctx: RunContext[SupportedDeps]):
    logger.info("Использован user_chat_history_tool")
    dialog_history = await get_data_from_db(user_id=ctx.deps.user_id)
    return dialog_history

@agent.system_prompt()
async def information_to_answer():
    logger.info("information_to_answer_sys_prompt")
    with open('app/text_to_answer.txt', 'r', encoding='utf-8') as file:
        return file.read()
