import subprocess
import numpy as np
import time
import psutil
import os
from ip_analyzer import get_ip_locations
def retrieve_ips():
    try:
        result = subprocess.run(
            ['powershell.exe', "-Command", "netstat -ano"],
            capture_output=True,
            text=True,
            check=True
        )
        ips = set()
        for line in result.stdout.strip().split('\n'):
            if "TCP" in line or "UDP" in line:
                parts = line.strip().split()
                if len(parts) >= 5:
                    addr = parts[2]
                    state = parts[3] if parts[0] == "TCP" else "N/A"
                    if '[' in addr and ']' in addr:
                        ip = addr.split(']')[0][1:]
                    elif ':' in addr:
                        ip = addr.split(':')[0]
                    elif '.' in addr:
                        ip = addr
                    else:
                        continue
                    if (
                        ip not in ("127.0.0.1", "0.0.0.0", "::1", "::")
                        and not ip.startswith(("192.168.", "10."))
                        and not (ip.startswith("172.") and 16 <= int(ip.split('.')[1]) <= 31)
                        and not ip.lower().startswith(("fc00:", "fd00:", "fe80:"))
                        and (state in ("ESTABLISHED", "TIME_WAIT") or parts[0] == "UDP")
                    ):
                        ips.add(ip)
        return np.array(sorted(ips)).reshape(-1, 1)
    except Exception:
        return np.array([])

def process_ram_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss // (1024 ** 2)
    return f"Current script RAM usage: {mem} MB"

if __name__ == "__main__":
    all_ips = set()
    while True:
        get_ip_locations()
        ram_usage = process_ram_usage()
        ips = retrieve_ips()
        for ip in ips.flatten():
            all_ips.add(ip)
        np.savetxt("external_ips.csv", np.array(sorted(all_ips)).reshape(-1, 1), fmt="%s", delimiter=",")
        msg = f"Total unique IPs collected: {len(all_ips)} | {ram_usage}"
        print(msg.ljust(80), end="\r", flush=True)
        print("\n[INFO] Program is running... (updates every 60 seconds)")
        get_ip_locations
        time.sleep(60)
