import socket

def scan_ports(target, start_port, end_port):
    print(f"Scanning ports on {target} from {start_port} to {end_port}...")
    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Timeout for the connection attempt

        try:
            result = sock.connect_ex((target, port))
            if result == 0:  # Port is open
                open_ports.append(port)
        except socket.error:
            pass
        finally:
            sock.close()

    if open_ports:
        print(f"Open ports found: {open_ports}")
    else:
        print("No open ports found.")

# Usage example:
if __name__ == "__main__":
    target_host = input("Enter the target IP or hostname: ")
    start = int(input("Enter the starting port number: "))
    end = int(input("Enter the ending port number: "))

    scan_ports(target_host, start, end)
