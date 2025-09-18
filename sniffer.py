#!/usr/bin/env python3
"""
sniffer.py
A simple, reasonably-safe packet sniffer using Scapy.

By default this prints only header info (IP/TCP/UDP/etc).
Optionally saves captured packets to a pcap file and can show a short payload preview.
"""

import argparse
import datetime
from scapy.all import sniff, wrpcap, IP, IPv6, TCP, UDP, Ether, Raw

captured = []

def human_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def summarize_packet(pkt, show_payload=False, max_payload=64):
    ts = human_time()
    eth = pkt.getlayer(Ether)
    ip = pkt.getlayer(IP) or pkt.getlayer(IPv6)
    proto = "Other"
    src = dst = "-"
    sport = dport = "-"
    length = len(pkt)
    extra = ""

    if ip:
        src = ip.src
        dst = ip.dst

    if pkt.haslayer(TCP):
        proto = "TCP"
        tcp = pkt.getlayer(TCP)
        sport = tcp.sport
        dport = tcp.dport
        flags = tcp.flags
        extra = f"flags={flags}"
    elif pkt.haslayer(UDP):
        proto = "UDP"
        udp = pkt.getlayer(UDP)
        sport = udp.sport
        dport = udp.dport
    else:
        # fallback: use highest layer name
        proto = pkt.lastlayer().name if pkt.lastlayer() else proto

    payload_preview = ""
    if show_payload and pkt.haslayer(Raw):
        raw = pkt.getlayer(Raw).load
        try:
            # show a short hex + ascii preview
            hexpart = raw[:max_payload].hex()
            asspart = ''.join((chr(b) if 32 <= b < 127 else '.') for b in raw[:max_payload])
            payload_preview = f" payload_preview(hex/ASCII)={hexpart} / {asspart}"
        except Exception:
            payload_preview = " payload_preview=<binary-unprintable>"

    return f"[{ts}] {proto:4} {src}:{sport} -> {dst}:{dport} len={length} {extra}{payload_preview}"

def packet_handler(pkt, args):
    # Only collect if the packet has an IP/IPv6 or is interesting
    captured.append(pkt)
    print(summarize_packet(pkt, show_payload=args.show_payload))
    if args.max_packets and len(captured) >= args.max_packets:
        # scapy sniff will stop automatically when return True from the callback if you do so,
        # but sniff() doesn't support that easily here. We'll rely on `stop_filter` below.
        pass

def stop_filter(pkt, args):
    if args.count <= 0:
        return False
    return len(captured) >= args.count

def main():
    parser = argparse.ArgumentParser(description="Simple header-focused network sniffer (Scapy).")
    parser.add_argument("-i", "--iface", help="Interface to capture on (default: Scapy default)", default=None)
    parser.add_argument("-f", "--filter", help="BPF filter (tcp, udp, port 80, host 1.2.3.4 ...)", default=None)
    parser.add_argument("-c", "--count", type=int, help="Number of packets to capture (0 for unlimited)", default=0)
    parser.add_argument("-o", "--output", help="Write captured packets to pcap file (optional)", default=None)
    parser.add_argument("--show-payload", action="store_true", help="Show a short payload preview (use cautiously)")
    args = parser.parse_args()

    if args.show_payload:
        print("WARNING: --show-payload will print part of packet payloads. Ensure you have permission to inspect contents.")
    print("Starting capture. Press Ctrl-C to stop.")
    try:
        sniff_kwargs = {
            "iface": args.iface,
            "filter": args.filter,
            "prn": lambda pkt: packet_handler(pkt, args),
            "store": False  # we store in our own list to control memory if desired
        }

        # If count > 0, use stop_filter to stop after capturing that many packets.
        if args.count > 0:
            sniff_kwargs["stop_filter"] = lambda pkt: stop_filter(pkt, args)
            # also pass count so the handler and stop_filter know
            args.max_packets = args.count
        else:
            args.max_packets = 0

        sniff(**sniff_kwargs)

    except KeyboardInterrupt:
        print("\nCapture interrupted by user.")
    except PermissionError:
        print("Permission denied. Try running as root/administrator (or pick a privileged interface).")
        return
    except Exception as e:
        print("Error while capturing:", e)

    if captured:
        print(f"Captured {len(captured)} packets.")
        if args.output:
            try:
                wrpcap(args.output, captured)
                print(f"Wrote packets to {args.output}")
            except Exception as e:
                print("Failed to write pcap:", e)
    else:
        print("No packets captured.")

if __name__ == "__main__":
    main()
