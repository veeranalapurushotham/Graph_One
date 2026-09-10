import argparse,asyncio
from datetime import datetime,timezone
from .config import Settings
from .http_client import AsyncHttpClient
from .extractors import extract_main_text,meta_date
from .dates import normalize_date,is_fresh_24h
from .llm import LLMOrchestrator
from .resolver import EntityResolver,DEFAULT_SEED
from .sources import NEWS_SOURCES,JOB_SOURCES,PAPER_SOURCES
async def run(hours=24,concurrency=40):
    settings=Settings(max_concurrency=concurrency); client=AsyncHttpClient(settings.max_concurrency,settings.request_timeout,settings.user_agent)
    urls=[s.url for s in NEWS_SOURCES+JOB_SOURCES+PAPER_SOURCES]; pages=await client.gather(urls); now=datetime.now(timezone.utc)
    fresh=[]
    for url,html in pages:
        dt=normalize_date(meta_date(html),now)
        if dt and is_fresh_24h(dt,now):fresh.append((url,extract_main_text(html),dt))
    resolver=EntityResolver(DEFAULT_SEED); llm=LLMOrchestrator(['gemini-flash','groq-llama3','deepseek'],settings.max_llm_concurrency)
    print(f'Fetched {len(pages)} source pages; {len(fresh)} passed 24-hour freshness.')
    print('Next: chunk -> verified LLM extraction -> entity resolution -> durable storage.')
    print(f'Seed resolver loaded with {len(resolver.seed)} canonical entities.')
    return fresh
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--hours',type=int,default=24); p.add_argument('--concurrency',type=int,default=40); a=p.parse_args(); asyncio.run(run(a.hours,a.concurrency))
