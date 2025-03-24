import nmap
import socket
from typing import List


def tcp_port_scan(target_ip: str, ports: List[int]) -> None:
    """
    Perform a TCP SYN scan (or fallback to TCP Connect) on the given IP and port list.

    Args:
        target_ip (str): Target IP address.
        ports (List[int]): List of ports to scan.
    """
    port_str = ",".join(str(p) for p in ports)
    scanner = nmap.PortScanner()

    print(f"\n[+] Starting TCP port scan on {target_ip} for ports: {port_str}")

    try:
        # Try SYN scan first (requires root/Administrator)
        scanner.scan(hosts=target_ip, arguments=f"-p {port_str} -sS")
    except Exception as e:
        print(f"[!] SYN scan failed: {e}")
        print("[*] Falling back to TCP Connect scan (-sT)...")
        scanner.scan(hosts=target_ip, arguments=f"-p {port_str} -sT")

    if target_ip in scanner.all_hosts():
        print(f"\nScan results for {target_ip}:\n")
        for proto in scanner[target_ip].all_protocols():
            ports = scanner[target_ip][proto].keys()
            for port in sorted(ports):
                state = scanner[target_ip][proto][port]['state']
                print(f"Port {port} is {state}")
    else:
        print(f"[!] No response from {target_ip}. Host may be unreachable.")


def dns_service_check(target_ip: str, port: int = 53, domain: str = "domain.xxx") -> None:
    """
    Attempt to resolve a domain using a custom DNS server and port.

    Args:
        target_ip (str): IP address of the DNS server to test.
        port (int): Port to test DNS on (default is 53).
        domain (str): Domain to resolve (default is domain.xxx).
    """
    print(f"\n[+] Testing DNS server at {target_ip}:{port} with query for {domain}")
    try:
        # Create a custom socket for DNS query
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        # Build a simple DNS query manually using dnspython (if available) or send garbage for test
        import dns.resolver
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [target_ip]
        resolver.port = port
        answer = resolver.resolve(domain)
        print(f"✅ DNS server responded. {domain} resolved to {[str(ip) for ip in answer]}")
    except Exception as e:
        print(f"❌ DNS test failed on {target_ip}:{port} — {e}")


if __name__ == "__main__":
    ip_target = "x.x.x.x"
    port_list = [25, 53, 443, 445, 8080, 8443]

    # Perform TCP port scan
    tcp_port_scan(ip_target, port_list)

    # Check DNS response
    dns_service_check(ip_target, port=53, domain="domain.xxx")
