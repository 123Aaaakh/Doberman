```bash
░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
```                                                                                                                     
*Before you use it, it's better to go straight to the "Dog" folder because there the code has become all-in-one. But if you want to use it one by one, that's also possible (if you use it one by one, for the IP in "portfinder.py" you should change it first)*

![Screenshot_2025-04-28_05-57-51](https://github.com/user-attachments/assets/d6c3e4bf-da62-40ac-8269-77a7da872ffe)



# [:]Doberman Scanner

A multifunctional **network reconnaissance toolkit** focused on SSDP/UPnP discovery and port scanning.

---

## Description
**Doberman Scanner** combines:
- Passive SSDP sniffing
- Active SSDP discovery
- UPnP device/service enumeration
- Custom TCP & UDP port scanning via Nmap

---

# [:]Doberman Cracking

This tool automates the entire process of scanning, capturing WPA/WPA2 handshakes, and cracking the Wi-Fi password using either CPU (aircrack-ng) or GPU (hashcat) with mask attack options.

It is designed for penetration testers who want a fast, flexible, and efficient way to test Wi-Fi security.

---

## Description
**Doberman Cracking** features:
- Auto enable monitor mode.
- Scan Wi-Fi networks.
- Capture WPA/WPA2 handshake using airodump-ng.
- Convert capture file to .22000 format using hcxpcapngtool.
- Crack password using:
- CPU with aircrack-ng
- GPU with hashcat (mask attack supported)
- Auto disable monitor mode and restart network services.


## Key Features
| Feature               |               Description                         |
|-----------------------|---------------------------------------------------|
| Passive SSDP Sniff    | Capture SSDP packets without active probing       |
| Active SSDP Scan      | Send M-SEARCH requests to the local network       |
| UPnP Fetch            | Retrieve and parse UPnP XML service descriptions  |
| Port Scanning         | Use Nmap to scan TCP/UDP ports                    |
| Cracking WIFI (2 Mode)| Use aircrack-ng and hashcat                       |

---

## Dependencies / Modules
Install via:
```bash
sudo apt update
sudo apt install aircrack-ng hcxtools hashcat
```

```bash
pip install colorama requests
```

**Python Modules:**
- `colorama`
- `requests`
- `subprocess` → to run `nmap` and `tshark`
- `socket`
- `xml.etree.ElementTree`
- `re`, `sys`, `time`, `os`
- `shutil`

**External Tools (must be installed):**
- `nmap`
- `tshark`
- `airmon-ng`, `airodump-ng`, `aireplay-ng`, `aircrack-ng (Aircrack-ng suite)`
- `hashcat`
- `hcxtools`

---

## Tips
- Run the script as `sudo` for optimal use of `tshark` and `nmap`
- Tested on Linux, but can be ported to Windows (with slight adjustments)
- Wi-Fi cracking should be used only on networks you own or are authorized to test
> ⚠️**Important: When hacking WiFi using brute force, it is better to have enough CPU because it uses a lot of CPU, and it is also better to use a capable GPU.**
>> ⚠️**Important: If you are using a virtual machine, make sure your USB Wi-Fi adapter is correctly passed through.**

---

## 🔹 Example Run
```bash
-> cd Doberman-main/
-> cd Dog/
-> sudo python3 Dobberman.py
```

## 🔹 To exit monitor mode
```bash
chmod +x monitor.sh
sudo ./monitor.sh {Your Interface} stop
```

---

# [!]For Manual Mask Attack Only (Mask.sh)

## 1.Make the script executable & Run interactively:
```bash
chmod +x Mash.sh
sudo ./Mask.sh
```

## 2.Follow the interactive prompts to:
- Choose capture file .22000
- Input your custom mask pattern

## 3.Example mask:
```bash
?u?u?u?u?u?d?d?d
```

---

## Coming Soon
- Export results to file (JSON/CSV)
- Automatic vulnerable device detection
- GUI version using tkinter/Flask (upon request)

---

**Happy Hacking!**
