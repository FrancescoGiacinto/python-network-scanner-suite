from scapy.all import IP, UDP, DNS, DNSQR, sr1
import os
from typing import List


def dns_query(domain: str, target_ip: str = "8.8.8.8", dport: int = 53, timeout: int = 1) -> List[str]:
    """
    Perform a stealthy DNS A-record lookup using Scapy.

    Args:
        domain (str): Domain name to resolve.
        target_ip (str): DNS server to query (default: 8.8.8.8).
        dport (int): Destination port (default: 53).
        timeout (int): Timeout in seconds.

    Returns:
        List[str]: List of IP addresses as strings.
    """
    pkt = IP(dst=target_ip) / UDP(dport=dport) / DNS(rd=1, qd=DNSQR(qname=domain))
    response = sr1(pkt, verbose=0, timeout=timeout)
    
    results = []
    if response and response.haslayer(DNS) and response[DNS].ancount > 0:
        for i in range(response[DNS].ancount):
            rr = response[DNS].an[i]
            if rr.type == 1:  # A record
                results.append(rr.rdata)
    return results


def reverse_dns_query(ip: str, target_ip: str = "8.8.8.8", dport: int = 53, timeout: int = 1) -> List[str]:
    """
    Perform a stealthy reverse DNS (PTR) lookup using Scapy.

    Args:
        ip (str): IP address to resolve.
        target_ip (str): DNS server to query (default: 8.8.8.8).
        dport (int): Destination port.
        timeout (int): Timeout for response.

    Returns:
        List[str]: List of resolved PTR names.
    """
    try:
        rev_ip = '.'.join(reversed(ip.split('.'))) + ".in-addr.arpa"
        pkt = IP(dst=target_ip) / UDP(dport=dport) / DNS(rd=1, qd=DNSQR(qname=rev_ip, qtype="PTR"))
        response = sr1(pkt, verbose=0, timeout=timeout)

        results = []
        if response and response.haslayer(DNS) and response[DNS].ancount > 0:
            for i in range(response[DNS].ancount):
                rr = response[DNS].an[i]
                if rr.type == 12:  # PTR record
                    results.append(rr.rdata.decode())
        return results
    except Exception:
        return []


def search_subdomains(base_domain: str, subdomains: List[str], include_numbers: bool = True) -> None:
    print(f"\n[+] Starting stealth DNS scan on: {base_domain}")
    for sub in subdomains:
        domains = [f"{sub}.{base_domain}"]
        if include_numbers:
            domains += [f"{sub}{i}.{base_domain}" for i in range(10)]

        for fqdn in domains:
            ips = dns_query(fqdn)
            if ips:
                print(f"\n✅ {fqdn} → {', '.join(ips)}")
                for ip in ips:
                    reverse = reverse_dns_query(ip)
                    if reverse:
                        print(f"   ↳ PTR for {ip}: {', '.join(reverse)}")


def load_subdomains(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
        return []


if __name__ == "__main__":
    domain = "google.com"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(script_dir, "subdomains.txt")
    subs = load_subdomains(wordlist_path)

    if subs:
        search_subdomains(domain, subs, include_numbers=True)
    else:
        print("[!] Subdomain list is empty.")
