import paramiko
import telnetlib
import os
from typing import Optional


def ssh_login(host: str, port: int, username: str, password: str) -> None:
    """
    Attempt to log in to an SSH server using provided credentials.

    Args:
        host (str): Target IP address or hostname.
        port (int): SSH port number (usually 22).
        username (str): Username for login.
        password (str): Password for login.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)

        ssh_session = ssh.get_transport().open_session()
        if ssh_session and ssh_session.active:
            print(f"[+] SSH login successful on {host}:{port} with {username}:{password}")
        ssh.close()
    except Exception as e:
        print(f"[-] SSH login failed for {username}:{password} — {e}")


def telnet_login(host: str, port: int, username: str, password: str) -> None:
    """
    Attempt to log in to a Telnet server using provided credentials.

    Args:
        host (str): Target IP address or hostname.
        port (int): Telnet port number (usually 23).
        username (str): Username for login.
        password (str): Password for login.
    """
    try:
        tn = telnetlib.Telnet(host, port, timeout=5)

        tn.read_until(b"login: ")
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        result = tn.expect([b"Last login", b"$", b"#"], timeout=5)
        if result[0] != -1:
            print(f"[+] Telnet login successful on {host}:{port} with {username}:{password}")
        else:
            print(f"[-] Telnet login failed for {username}:{password}")
        tn.close()
    except Exception as e:
        print(f"[-] Telnet connection failed for {username}:{password} — {e}")


def run_login_attempts(host: str, port: int, creds_file: str, use_ssh: bool = True, use_telnet: bool = True) -> None:
    """
    Attempt multiple logins using credentials from a file.

    Args:
        host (str): Target host IP or domain.
        port (int): Target port (will be used for both protocols).
        creds_file (str): Path to file containing username and password pairs.
        use_ssh (bool): Whether to perform SSH login attempts.
        use_telnet (bool): Whether to perform Telnet login attempts.
    """
    try:
        with open(creds_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                username, password = parts[0], parts[1]
                if use_ssh:
                    ssh_login(host, port, username, password)
                if use_telnet:
                    telnet_login(host, port, username, password)
    except FileNotFoundError:
        print(f"[!] Credentials file '{creds_file}' not found.")


# Example usage
if __name__ == "__main__":
    target_host = "x.x.x.x"
    target_port = 2200
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_file = os.path.join(script_dir, "defaults.txt")

    run_login_attempts(target_host, target_port, credentials_file)
