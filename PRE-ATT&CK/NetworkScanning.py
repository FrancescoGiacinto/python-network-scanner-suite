import nmap
import socket

# Initialize the Nmap scanner
nm = nmap.PortScanner()

# Target IP and domain
IPtarget: str = "8.8.8.8"
DNStarget: str = "google.com"
ports: str = "25,53,443,445,8080,8443"

def port_scan_tcp(target_ip: str, port_list: str) -> None:
    """
    Perform a TCP Connect Scan (-sS) on a given IP address and list of ports. It dont complete the handshake, just send a SYN packet.
    
    Args:
        target_ip (str): The IP address to scan.
        port_list (str): Comma-separated string of port numbers to scan.
    """
    print(f"\n[+] Scanning {target_ip} for ports: {port_list}")
    try:
        # TCP Connect scan (no admin privileges needed)
        nm.scan(hosts=target_ip, arguments=f"-p {port_list} -sS")

        if target_ip in nm.all_hosts():
            print(f"\nResults for {target_ip}:\n")
            for proto in nm[target_ip].all_protocols():
                ports = nm[target_ip][proto].keys()
                for port in sorted(ports):
                    state = nm[target_ip][proto][port]['state']
                    print(f"Port {port} is {state}")
        else:
            print(f"[!] No results for {target_ip}. The host may be unreachable.")

    except Exception as e:
        print(f"[ERROR] Port scan failed: {e}")

def dns_resolve(domain: str) -> None:
    """
    Resolve a domain name to its corresponding IP address using standard DNS.

    Args:
        domain (str): The domain name to resolve.
    """
    print(f"\n[+] Resolving domain: {domain}")
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"{domain} resolved to {ip_address}")
    except socket.gaierror:
        print(f"[!] Could not resolve domain: {domain}")

# Execute scans
dns_resolve(DNStarget)
port_scan_tcp(IPtarget, ports)
