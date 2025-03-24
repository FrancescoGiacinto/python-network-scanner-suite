import dns.resolver
import os
import socket
from typing import List


def reverse_dns(ip: str) -> List[str]:
    """
    Perform a reverse DNS lookup on an IP address.

    Args:
        ip (str): The IP address to resolve.

    Returns:
        List[str]: A list of domain names associated with the IP.
    """
    try:
        host_info = socket.gethostbyaddr(ip)
        primary = host_info[0]
        aliases = host_info[1]
        return [primary] + aliases
    except Exception:
        return []


def resolve_dns(domain: str) -> List[str]:
    """
    Perform a DNS A record lookup on a given domain.

    Args:
        domain (str): The fully qualified domain name to resolve.

    Returns:
        List[str]: List of IP addresses (as strings) for that domain.
    """
    try:
        result = dns.resolver.resolve(domain, "A")
        return [r.to_text() for r in result]
    except Exception:
        return []


def search_subdomains(base_domain: str, subdomains: List[str], include_numbers: bool = True) -> None:
    """
    Try to resolve common subdomains and optionally numbered subdomains.

    Args:
        base_domain (str): The domain to append subdomains to (e.g., 'domain.xxx').
        subdomains (List[str]): A list of subdomain prefixes to test (e.g., 'mail', 'vpn').
        include_numbers (bool): Whether to test numbered subdomains (e.g., 'www1', 'mail2').
    """
    print(f"\n[+] Starting DNS reconnaissance on: {base_domain}")
    for sub in subdomains:
        domains_to_check = [f"{sub}.{base_domain}"]

        if include_numbers:
            domains_to_check += [f"{sub}{i}.{base_domain}" for i in range(10)]

        for fqdn in domains_to_check:
            ip_list = resolve_dns(fqdn)
            if ip_list:
                print(f"\n✅ {fqdn} → {', '.join(ip_list)}")
                for ip in ip_list:
                    reverse = reverse_dns(ip)
                    if reverse:
                        print(f"   ↳ Reverse DNS for {ip}: {', '.join(reverse)}")


def load_subdomains(file_path: str) -> List[str]:
    """
    Load subdomains from a text file.

    Args:
        file_path (str): Path to the file containing subdomain prefixes.

    Returns:
        List[str]: List of subdomain strings.
    """
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
        return []


if __name__ == "__main__":
    base_domain = "domain.xxx"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(script_dir, "subdomains.txt")
    subdomain_list = load_subdomains(wordlist_path)


    if subdomain_list:
        search_subdomains(base_domain, subdomain_list, include_numbers=True)
    else:
        print("[!] No subdomains to scan.")
