import subprocess

target_ip = "192.168.110.229" #CHANGE THIS, for Your TARGET
udp_ports = "1900,1985,49152,5431,5555"
tcp_ports = "80,443,5000,49152,49153,5431,5555"

print(f"\n[🔍] Scanning TCP & UDP to {target_ip}\n")

def run_nmap(protocol: str, ports: str):
    print(f"[⚙️ ] Scanning {protocol.upper()} ports: {ports}")
    try:
        result = subprocess.run(
            [
                "sudo",
                "nmap",
                f"-s{protocol.upper()}",
                "-p",
                ports,
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
        print(f"[❌] Scan Failed {protocol.upper()}: {e.stderr}")
    except Exception as e:
        print(f"[❌] Another Error while scanning {protocol.upper()}: {e}")

run_nmap("t", tcp_ports)
run_nmap("u", udp_ports)

def passive_ssdp_sniff(interface="any"):
    print("[👂] Passive listening for SSDP (UDP 1900)... Press Ctrl+C to exit.")
    try:
        subprocess.run(
            [
                "sudo",
                "tshark",
                "-i",
                interface,
                "-Y",
                "udp.port == 1900",
                "-T",
                "fields",
                "-e",
                "ip.src",
                "-e",
                "udp.srcport",
                "-e",
                "data",
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[❌] tshark failed to run: {e.stderr}")
    except KeyboardInterrupt:
        print("\n[⛔] Stop listening.")
    except Exception as e:
        print(f"[❌] Another Errot while sniffing: {e}")

# passive_ssdp_sniff()