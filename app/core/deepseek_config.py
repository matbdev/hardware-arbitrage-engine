import os

from langchain_openrouter import ChatOpenRouter


def get_deepseek_model() -> ChatOpenRouter:
    """
    Returns the DeepSeek v4 Flash Free model using OpenRouter.
    """
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    if not api_key:
        raise ValueError('OPENROUTER_API_KEY environment variable is not set')

    llm = ChatOpenRouter(
        api_key=api_key,
        model='deepseek/deepseek-v4-flash:free',
        temperature=0,
        max_retries=5,
    )
    return llm
