from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()
@dataclass(frozen=True)
class Settings:
    request_timeout: int = int(os.getenv('REQUEST_TIMEOUT_SECONDS','30'))
    max_concurrency: int = int(os.getenv('MAX_CONCURRENCY','40'))
    max_llm_concurrency: int = int(os.getenv('MAX_LLM_CONCURRENCY','20'))
    max_chars_per_chunk: int = int(os.getenv('MAX_CHARS_PER_CHUNK','12000'))
    user_agent: str = os.getenv('USER_AGENT','GraphOneIntelligenceCrawler/1.0')
    gemini_key: str = os.getenv('GEMINI_API_KEY','')
    groq_key: str = os.getenv('GROQ_API_KEY','')
    deepseek_key: str = os.getenv('DEEPSEEK_API_KEY','')
