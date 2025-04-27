#!/usr/bin/env python3
import subprocess
import socket
import time
import requests
import xml.etree.ElementTree as ET
import re
import sys
import os
import glob
import shutil
from colorama import init, Fore


init(autoreset=True)
# ================= ASCII LOGO ================= #
def print_ascii_credit():
    print(Fore.RED + r"""                                                                                  
                                                       
░░░           ░                                        
░░    ▒      █                                         
░    ▒██▓▓▓▒██         ░                ▒█             
    ░█▓▒▓█████▓         █▒        ▓     ██     ░       
    ▓███▓▓████▓         ███████████     ██▓    ▓▒      
    ░████▒▓██░          █████▒▒▒▓██▒   ░███▓███▓▒▒     
     █████▓██▒          ▓██░░░███▒▓    ░████████▓▒██▓  
     ████████▓          ░██▒░█████▒     █████▓▓▓▓███▓  
     ▒███████▓          ▓█████████      █████▓▓█████   
     ▒███████░          █████████▒     ▓█████████      
     ▒█▓▓█▓▓▒▒          ▓████████▒    ░█████████       
     █████████         ░▒░▒░▓▒▓██░    ░ ▒██████░       
    ▒██████████       ▓█████████▓    ▓█▓▒░▓▓▓▓▒        
   ▒███████████░     ░███████████░  ▓█████████▒        
  ▓█████████████░    █████████████▓███████████▒        
 ████████████████   █████████████████████████▓█▒       
█████████████████▒ █████████████████████████████░

░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
        

     +==========================================+
     |                                          |
     |    Credit:                               |       
     |                                          |
     |       The Unknown people and @saxother   |                            
     |                                          |
     +==========================================+
    """)

def loading_animation(text="Loading", duration=3):
    print(Fore.RED + text, end="")
    for _ in range(duration * 3):
        sys.stdout.write(Fore.RED + ".")
        sys.stdout.flush()
        time.sleep(0.33)
    time.sleep(0.5)
    clear_screen()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
# ================ Passive SSDP Sniff ================ #
def sniff_ssdp_ips(interface='wlp4s0', duration=5):
    print("[*] Sniffing SSDP IPs via tshark...")
    cmd = ["tshark", "-i", interface, "-Y", 'udp contains "ssdp"', "-T", "fields", "-e", "ip.src", "-l"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    ips = set()
    start = time.time()

    while True:
        line = proc.stdout.readline()
        if line:
            ip = line.strip()
            if ip:
                ips.add(ip)
        if time.time() - start > duration:
            proc.terminate()
            break
    return list(ips)

# ================ SSDP Active Scan & UPnP Description ================ #
def send_ssdp_probe(ip):
    print(f"\n[→] Scanning SSDP: {ip}")
    ssdp_request = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        f'HOST: {ip}:1900',
        'MAN: "ssdp:discover"',
        'MX: 2',
        'ST: ssdp:all',
        '', ''
    ]).encode('utf-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.sendto(ssdp_request, (ip, 1900))
        data, addr = sock.recvfrom(4096)
        response = data.decode(errors='ignore')
        print(f"[+] Respon dari {addr[0]}")
        return parse_location(response)
    except socket.timeout:
        print("[!] No SSDP response.")
        return None
    finally:
        sock.close()

def parse_location(response):
    for line in response.split('\r\n'):
        if line.lower().startswith("location:"):
            location = line.split(":", 1)[1].strip()
            print(f"    📍 LOCATION: {location}")
            return location
    return None

def fetch_upnp_description(url):
    print("    🔍 Fetching UPnP Description...")
    try:
        res = requests.get(url, timeout=3)
        root = ET.fromstring(res.content)
        ns = {'upnp': 'urn:schemas-upnp-org:device-1-0'}

        device = root.find(".//upnp:device", ns)
        if device is not None:
            print("     Device Info:")
            print(f"      → Friendly Name: {device.findtext('upnp:friendlyName', default='-', namespaces=ns)}")
            print(f"      → Manufacturer:  {device.findtext('upnp:manufacturer', default='-', namespaces=ns)}")
            print(f"      → Model Name:    {device.findtext('upnp:modelName', default='-', namespaces=ns)}")
            print(f"      → Device Type:   {device.findtext('upnp:deviceType', default='-', namespaces=ns)}")
        else:
            print("    [!] No <device> section found.")
    except Exception as e:
        print(f"    [X] Failed take the Description: {e}")

# ================ SSDP Broadcast Discovery ================ #
def discover_upnp_devices(timeout=3, interface="0.0.0.0"):
    ssdp_request = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST: 239.255.255.250:1900\r\n"
        "MAN: \"ssdp:discover\"\r\n"
        "MX: 2\r\n"
        "ST: upnp:rootdevice\r\n"
        "\r\n"
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(timeout)

    try:
        sock.bind((interface, 0))
    except Exception as e:
        print(f"[X] Failed to bind in Interface {interface}: {e}")
        return []

    sock.sendto(ssdp_request.encode(), ("239.255.255.250", 1900))
    print("[→] Giving SSDP Probe...")

    locations = set()
    start = time.time()
    while True:
        try:
            data, addr = sock.recvfrom(65507)
            match = re.search(r"LOCATION: (.*)", data.decode("utf-8", errors="ignore"), re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                print(f"[+] Respond from {addr[0]}\n     LOCATION: {location}")
                locations.add(location)
        except socket.timeout:
            break
        if time.time() - start > timeout:
            break

    return list(locations)

def fetch_upnp_services(location_url):
    print(f" Fetching UPnP Description from {location_url}")
    try:
        res = requests.get(location_url, timeout=5)
        xml = ET.fromstring(res.content)

        ns = {'urn': 'urn:schemas-upnp-org:device-1-0'}
        device = xml.find('.//urn:device', ns)
        if device is not None:
            print(" Device Info:")
            print("  → Friendly Name:", device.findtext('urn:friendlyName', default='-', namespaces=ns))
            print("  → Manufacturer: ", device.findtext('urn:manufacturer', default='-', namespaces=ns))
            print("  → Model Name:   ", device.findtext('urn:modelName', default='-', namespaces=ns))
            print("  → Device Type:  ", device.findtext('urn:deviceType', default='-', namespaces=ns))

        service_list = xml.findall('.//urn:service', ns)
        for service in service_list:
            service_type = service.findtext('urn:serviceType', default='-', namespaces=ns)
            control_url = service.findtext('urn:controlURL', default='-', namespaces=ns)
            print(f"    [!] Service: {service_type}\n       Control URL: {control_url}")
    except Exception as e:
        print("[X] failed to take and parsing UPnP XML:", e)

# ================ Port Scanning ================ #
def run_nmap_scan(target_ip, tcp_ports, udp_ports):
    def run_nmap(protocol: str, ports: str):
        print(f"[!] Scanning {protocol.upper()} ports: {ports}")
        try:
            result = subprocess.run(
                [
                    "sudo",
                    "nmap",
                    f"-s{protocol.upper()}",
                    "-p", ports,
                    "-Pn",
                    "--open",
                    "--reason",
                    target_ip,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"[X] Scan failed {protocol.upper()}: {e.stderr}")
        except Exception as e:
            print(f"[X] Error while another scan {protocol.upper()}: {e}")

    run_nmap("t", tcp_ports)
    run_nmap("u", udp_ports)

def passive_ssdp_sniff(interface="any"):
    print("[!] Passive listening for SSDP (UDP 1900)... Press CTRL+C to exit.")
    try:
        subprocess.run(
            [
                "sudo", "tshark", "-i", interface, # While use another distro in Linux or windows maybe sudo can be removed
                "-Y", "udp.port == 1900",
                "-T", "fields",
                "-e", "ip.src", "-e", "udp.srcport", "-e", "data",
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[X] tshark failed to run: {e.stderr}")
    except KeyboardInterrupt:
        print("\n[!] Stop listening.")
    except Exception as e:
        print(f"[X] Error while another sniffing: {e}")


# ==================WIFI====================== #

def enable_monitor_mode(interface):
    print(f"[+] Enabling monitor mode on {interface}...")
    try:
        subprocess.run(["airmon-ng", "check", "kill"], check=True)
        subprocess.run(["airmon-ng", "start", interface], check=True)
    except subprocess.CalledProcessError:
        print("[!] Failed to enable monitor mode. Check interface or run with sudo.")
        return False
    return True

def scan_wifi(interface):
    print("[+] Scanning for nearby Wi-Fi networks...")
    print("[*] Press Ctrl+C after you've spotted your target.")
    time.sleep(2)
    try:
        subprocess.run(["airodump-ng", interface], check=True)
    except KeyboardInterrupt:
        print("[!] Scan stopped.")

def capture_handshake(interface, bssid, channel, output_base="handshake"):
    print(f"[+] Capturing handshake for BSSID {bssid} on channel {channel}...")
    proc = subprocess.Popen([
        "airodump-ng",
        "-c", channel,
        "--bssid", bssid,
        "-w", output_base,
        interface
    ])
    print("[*] Wait until you see 'WPA handshake' captured at the top right...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()
        print("[!] Capture stopped.")

def find_latest_handshake_file(base_name="handshake"):
    cap_files = sorted(glob.glob(f"{base_name}-*.cap"), key=os.path.getmtime, reverse=True)
    return cap_files[0] if cap_files else None

def crack_handshake_aircrack(capture_file, wordlist):
    print("[+] Cracking WPA handshake using aircrack-ng (CPU)...")
    try:
        subprocess.run(["aircrack-ng", "-w", wordlist, capture_file], check=True)
    except subprocess.CalledProcessError:
        print("[!] Cracking failed or password not found.")

def crack_handshake_hashcat(capture_file, wordlist):
    print("[+] Converting cap to 22000 format (hc22000)...")
    hccapx_file = "handshake.22000"

    if not shutil.which("hcxpcapngtool"):
        print("[!] hcxpcapngtool not found. Please install hcxtools.")
        return

    try:
        subprocess.run(["hcxpcapngtool", "-o", hccapx_file, capture_file], check=True)
    except subprocess.CalledProcessError:
        print("[!] hcxpcapngtool failed during conversion.")
        return

    print("[+] Running hashcat (GPU, mode 22000)...")
    try:
        subprocess.run(["hashcat", "-m", "22000", hccapx_file, wordlist, "--force"], check=True)
    except subprocess.CalledProcessError:
        print("[!] Hashcat failed or password not found.")

def wifi_crack_menu():
    iface = input("[?] Enter your wireless interface (e.g. wlan0): ").strip()
    if not iface:
        print("[!] Invalid interface.")
        return

    if not enable_monitor_mode(iface):
        return

    mon_iface = iface + "mon"
    scan_wifi(mon_iface)

    bssid = input("[?] Target BSSID: ").strip()
    if not bssid:
        print("[!] Invalid BSSID.")
        return

    channel = input("[?] Channel: ").strip()
    if not channel.isdigit():
        print("[!] Invalid channel.")
        return

    capture_base = "handshake"
    capture_handshake(mon_iface, bssid, channel, output_base=capture_base)

    capture_file = find_latest_handshake_file(capture_base)
    if not capture_file:
        print("[!] No .cap file found. Make sure handshake was captured.")
        return

    print(f"[+] Found capture file: {capture_file}")

    wordlist = input("[?] Path to wordlist (e.g. /usr/share/wordlists/rockyou.txt): ").strip()
    if not wordlist or not os.path.isfile(wordlist):
        print("[!] Wordlist file not found.")
        return

    print("[+] Choose cracking method:")
    print("    [1] CPU (aircrack-ng)")
    print("    [2] GPU (hashcat)")
    crack_mode = input("[?] Crack using [1/2]: ").strip()
    if crack_mode == "2":
        crack_handshake_hashcat(capture_file, wordlist)
    else:
        crack_handshake_aircrack(capture_file, wordlist)

def wifi_crack_main():
    wifi_crack_menu()

# ================ MENU ================ #
def main():
    print_ascii_credit()
    loading_animation("Initializing Doberman Engine", duration=3)
    # Lanjut ke menu atau proses lain
    print("\n[✅] System Ready, Starting the menu...\n")
    print_ascii_credit()
    while True:
        print("\n Menu:")
        print("1. Passive SSDP Sniffing")
        print("2. Active SSDP Scaner")
        print("3. Discover UPnP Devices")
        print("4. Nmap Port Scan")
        print("5. WIFI cracking")
        print("6. exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            iface = input("Interface (default: any): ").strip() or "any"
            passive_ssdp_sniff(iface)
        elif choice == "2":
            iface = input("Interface (default: wlp4s0): ").strip() or "wlp4s0"
            ips = sniff_ssdp_ips(iface)
            for ip in ips:
                loc = send_ssdp_probe(ip)
                if loc:
                    fetch_upnp_description(loc)
        elif choice == "3":
            iface = input("Interface (default: 0.0.0.0): ").strip() or "0.0.0.0"
            timeout = input("Timeout (default: 3): ").strip()
            timeout = int(timeout) if timeout.isdigit() else 3
            locs = discover_upnp_devices(timeout, iface)
            for loc in locs:
                fetch_upnp_services(loc)
        elif choice == "4":
            target_ip = input("Target IP (default: 192.168.1.1): ").strip() or "192.168.1.1"
            tcp_ports = input("TCP Ports (default: 80,443,5000): ").strip() or "80,443,5000"
            udp_ports = input("UDP Ports (default: 1900,1985): ").strip() or "1900,1985"
            run_nmap_scan(target_ip, tcp_ports, udp_ports)
        elif choice == "5":
            wifi_crack_main()
        elif choice == "6":
            print("Bye, woof!")
            break
        else:
            print("[!] No valid selection.")

if __name__ == "__main__":
        main()