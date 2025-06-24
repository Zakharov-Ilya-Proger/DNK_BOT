from app.ai.ai_agent_setup import agent, SupportedDeps
from app.db.db import insert


async def generate_response(user_id: int, current_message: str):
    deps = SupportedDeps(user_id=user_id)
    result = await agent.run(current_message, deps=deps)
    await insert(user_id, result, "system")
    await  insert(user_id, current_message, "user")
    return result