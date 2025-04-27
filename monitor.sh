#!/bin/bash

# Monitor Mode Toggle Script

if [[ $EUID -ne 0 ]]; then
   echo "[!] Please run as root (sudo)."
   exit 1
fi

INTERFACE=$1

if [ -z "$INTERFACE" ]; then
    echo "Usage: sudo ./monitor.sh <interface> <on|off>"
    echo "Example: sudo ./monitor.sh wlan0 on"
    echo "         sudo ./monitor.sh wlan0 off"
    exit 1
fi

MODE=$2

if [ -z "$MODE" ]; then
    echo "[!] Missing mode: on or off"
    echo "Usage: sudo ./monitor.sh <interface> <on|off>"
    exit 1
fi

if [ "$MODE" == "on" ]; then
    echo "[+] Enabling monitor mode on $INTERFACE..."
    airmon-ng check kill
    airmon-ng start "$INTERFACE"
elif [ "$MODE" == "off" ]; then
    MONITOR_IFACE=$(iwconfig 2>/dev/null | grep -B1 "Mode:Monitor" | grep -oE '^[^ ]+')
    if [ -z "$MONITOR_IFACE" ]; then
        MONITOR_IFACE="${INTERFACE}mon"
    fi
    echo "[+] Disabling monitor mode on $MONITOR_IFACE..."
    airmon-ng stop "$MONITOR_IFACE"
    echo "[+] Restarting NetworkManager..."
    systemctl restart NetworkManager
else
    echo "Usage: sudo ./monitor.sh <interface> <on|off>"
    echo "Example: sudo ./monitor.sh wlan0 on"
    echo "         sudo ./monitor.sh wlan0 off"
    exit 1
fi