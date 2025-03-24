import nmap
import socket

nm = nmap.PortScanner()
IPtarget = "8.8.8.8"
DNStarget = "google.com"
ports = "25,53,443,445,8080,8443"

def PortScan_TCP(IPtarget, ports):
    print(f"\n[+] Scanning {IPtarget} for ports: {ports}")
    try:
        nm.scan(hosts=IPtarget, arguments=f"-p {ports} -sT")

        if IPtarget in nm.all_hosts():
            print(f"\nResults for {IPtarget}:\n")
            for proto in nm[IPtarget].all_protocols():
                lport = nm[IPtarget][proto].keys()
                for port in sorted(lport):
                    state = nm[IPtarget][proto][port]['state']
                    print(f"Port {port} is {state}")
        else:
            print(f"[!] No results for {IPtarget}. Host may be unreachable.")

    except Exception as e:
        print(f"[ERROR] Port scan failed: {e}")

def DNSResolve(domain):
    print(f"\n[+] Resolving domain: {domain}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{domain} resolved to {ip}")
    except socket.gaierror:
        print(f"[!] Could not resolve domain: {domain}")

# Run scans
DNSResolve(DNStarget)
PortScan_TCP(IPtarget, ports)
