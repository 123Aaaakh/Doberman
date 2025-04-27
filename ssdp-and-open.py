import socket
import requests
import xml.etree.ElementTree as ET
import time
import re

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
        print(f"[❌] Gagal bind ke interface {interface}: {e}")
        return []

    sock.sendto(ssdp_request.encode(), ("239.255.255.250", 1900))

    print("[→] Mengirim SSDP probe...")

    locations = set()
    start = time.time()
    while True:
        try:
            data, addr = sock.recvfrom(65507)
            match = re.search(r"LOCATION: (.*)", data.decode("utf-8", errors="ignore"), re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                print(f"[+] Respon dari {addr[0]}\n    F4CD LOCATION: {location}")
                locations.add(location)
        except socket.timeout:
            break
        if time.time() - start > timeout:
            break

    return list(locations)

def fetch_upnp_services(location_url):
    print(f"🔍 Fetching UPnP Description from {location_url}")
    try:
        res = requests.get(location_url, timeout=5)
        xml = ET.fromstring(res.content)

        ns = {'urn': 'urn:schemas-upnp-org:device-1-0'}
        device = xml.find('.//urn:device', ns)
        if device is not None:
            print("🧠 Device Info:")
            print("  → Friendly Name:", device.findtext('urn:friendlyName', default='-', namespaces=ns))
            print("  → Manufacturer: ", device.findtext('urn:manufacturer', default='-', namespaces=ns))
            print("  → Model Name:   ", device.findtext('urn:modelName', default='-', namespaces=ns))
            print("  → Device Type:  ", device.findtext('urn:deviceType', default='-', namespaces=ns))

        service_list = xml.findall('.//urn:service', ns)
        for service in service_list:
            service_type = service.findtext('urn:serviceType', default='-', namespaces=ns)
            control_url = service.findtext('urn:controlURL', default='-', namespaces=ns)
            print(f"    🔧 Service: {service_type}\n       Control URL: {control_url}")
    except Exception as e:
        print("[❌] Gagal ambil dan parsing UPnP XML:", e)

if __name__ == "__main__":
    iface = input("[?] Masukkan interface lokal (default 0.0.0.0): ").strip() or "0.0.0.0"
    timeout = input("[?] Masukkan waktu timeout (default 3 detik): ").strip()
    try:
        timeout = int(timeout)
    except ValueError:
        timeout = 3

    locations = discover_upnp_devices(timeout=timeout, interface=iface)
    if not locations:
        print("[!] Tidak ada UPnP device ditemukan.")
    else:
        for loc in locations:
            fetch_upnp_services(loc)