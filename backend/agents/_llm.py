
from config.settings import settings
import os, litellm

def chat_completion(messages):
    provider = settings.llm_provider.lower()

    # mock mode if no key or provider explicitly "mock"
    if provider == "mock" or (provider == "openai" and not settings.openai_api_key):
        # deterministic mock for local tests
        return {"choices":[{"message":{"content":"{\"paragraphs\":[\"Mock paragraph 1\",\"Mock paragraph 2\",\"Mock paragraph 3\"],\"whats_new\":[\"Mock new 1\",\"Mock new 2\"],\"open_problems\":[\"Mock open 1\"],\"top5_papers\":[{\"title\":\"Mock\",\"url\":\"http://example.com\"}]}"}}]}

    if settings.openai_project_id:
        os.environ["OPENAI_PROJECT_ID"] = settings.openai_project_id

    if provider == "openai":
        return litellm.completion(model=settings.openai_model, messages=messages)

    if provider == "ollama":
        return litellm.completion(model=f"ollama/{settings.ollama_model}", messages=messages)

    # fallback mock
    return {"choices":[{"message":{"content":"{\"paragraphs\":[\"Fallback 1\",\"Fallback 2\",\"Fallback 3\"],\"whats_new\":[\"A\",\"B\"],\"open_problems\":[\"C\"],\"top5_papers\":[{\"title\":\"T\",\"url\":\"U\"}]}"}}]}
