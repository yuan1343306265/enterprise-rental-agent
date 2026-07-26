from langchain_deepseek import ChatDeepSeek
from app.config import settings


llm = ChatDeepSeek(
    model=settings.model_name,
    api_key=settings.deepseek_api_key,
    base_url=settings.deepseek_base_url,
    temperature=0,
    timeout=30,
    max_retries=2,
)