import asyncio,random
import aiohttp
class AsyncHttpClient:
    def __init__(self,concurrency=40,timeout=30,user_agent='GraphOneCrawler/1.0'):
        self.sem=asyncio.Semaphore(concurrency); self.timeout=aiohttp.ClientTimeout(total=timeout)
        self.headers={'User-Agent':user_agent,'Accept':'text/html,application/json;q=0.9,*/*;q=0.8'}
    async def get_text(self,session,url,attempts=5):
        async with self.sem:
            for attempt in range(attempts):
                try:
                    async with session.get(url,timeout=self.timeout,headers=self.headers) as r:
                        if r.status in (429,500,502,503,504):
                            ra=r.headers.get('Retry-After'); delay=float(ra) if ra and ra.isdigit() else min(30,2**attempt)
                            await asyncio.sleep(delay+random.uniform(0,.5)); continue
                        r.raise_for_status(); return await r.text(errors='replace')
                except (aiohttp.ClientError,asyncio.TimeoutError):
                    if attempt==attempts-1: raise
                    await asyncio.sleep(min(30,2**attempt)+random.uniform(0,.5))
            raise RuntimeError(f'Failed to fetch {url}')
    async def gather(self,urls):
        async with aiohttp.ClientSession() as session:
            results=await asyncio.gather(*(self.get_text(session,u) for u in urls),return_exceptions=True)
        return [(u,r) for u,r in zip(urls,results) if isinstance(r,str)]
