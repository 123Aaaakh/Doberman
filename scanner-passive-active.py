import subprocess
import socket
import time
import requests
import xml.etree.ElementTree as ET

def sniff_ssdp_ips(interface='wlp4s0', duration=5):
    print("[*] Sniffing SSDP IPs via tshark...")
    cmd = [
        "tshark", "-i", interface,
        "-Y", 'udp contains "ssdp"',
        "-T", "fields", "-e", "ip.src", "-l"
    ]
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
            print("    🧠 Device Info:")
            print(f"      → Friendly Name: {device.findtext('upnp:friendlyName', default='-', namespaces=ns)}")
            print(f"      → Manufacturer:  {device.findtext('upnp:manufacturer', default='-', namespaces=ns)}")
            print(f"      → Model Name:    {device.findtext('upnp:modelName', default='-', namespaces=ns)}")
            print(f"      → Device Type:   {device.findtext('upnp:deviceType', default='-', namespaces=ns)}")
        else:
            print("    ⚠️ No <device> section found.")
    except Exception as e:
        print(f"    ❌ Gagal ambil deskripsi: {e}")


if __name__ == "__main__":
    interface = "wlp4s0"  # Ganti sesuai interface kamu
    ip_list = sniff_ssdp_ips(interface)

    if not ip_list:
        print("[!] Tidak ada IP SSDP terdeteksi.")
    else:
        for ip in ip_list:
            location_url = send_ssdp_probe(ip)
            if location_url:
                fetch_upnp_description(location_url)
