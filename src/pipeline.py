import argparse, asyncio
from datetime import datetime, timezone
from pathlib import Path
from .config import Settings
from .http_client import AsyncHttpClient
from .extractors import extract_main_text, meta_date
from .dates import normalize_date, is_fresh_24h
from .llm import LLMOrchestrator
from .resolver import EntityResolver, DEFAULT_SEED
from .sources import NEWS_SOURCES, JOB_SOURCES, PAPER_SOURCES

async def run(hours=24, concurrency=40, output_dir='output'):
    settings = Settings(max_concurrency=concurrency)
    client = AsyncHttpClient(
        settings.max_concurrency,
        settings.request_timeout,
        settings.user_agent,
    )
    sources = NEWS_SOURCES + JOB_SOURCES + PAPER_SOURCES
    pages = await client.gather([s.url for s in sources])
    now = datetime.now(timezone.utc)
    source_by_url = {s.url: s for s in sources}
    fresh = []

    for url, html in pages:
        dt = normalize_date(meta_date(html), now)
        if dt and is_fresh_24h(dt, now):
            source = source_by_url[url]
            fresh.append({
                'source': source.name,
                'kind': source.kind,
                'url': url,
                'collected_at': now.isoformat(),
                'published_at': dt.isoformat(),
                'text': extract_main_text(html),
            })

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    output_file = out / 'fresh_source_pages.jsonl'
    with output_file.open('w', encoding='utf-8') as f:
        import json
        for record in fresh:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    resolver = EntityResolver(DEFAULT_SEED)
    LLMOrchestrator(
        ['gemini-flash', 'groq-llama3', 'deepseek'],
        settings.max_llm_concurrency,
    )
    print(f'Fetched {len(pages)} source pages; {len(fresh)} passed 24-hour freshness.')
    print(f'Fresh source pages written to {output_file}.')
    print('Next: chunk -> verified LLM extraction -> entity resolution -> durable storage.')
    print(f'Seed resolver loaded with {len(resolver.seed)} canonical entities.')
    return fresh

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--hours', type=int, default=24)
    p.add_argument('--concurrency', type=int, default=40)
    p.add_argument('--output-dir', default='output')
    a = p.parse_args()
    asyncio.run(run(a.hours, a.concurrency, a.output_dir))
