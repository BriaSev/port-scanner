import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import socket
import pandas as pd
import threading
import queue
import os
from datetime import datetime

class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner")
        self.results = []
        self.output_dir = os.getcwd()  # Default output directory
        self.queue = queue.Queue()
        self.scanning = False

        # Menu Bar
        menubar = tk.Menu(root)
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Set Output Directory", command=self.set_output_dir)
        menubar.add_cascade(label="Options", menu=options_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        menubar.add_cascade(label="Help", menu=help_menu)
        root.config(menu=menubar)

        # IP Input
        tk.Label(root, text="Target IP:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = tk.Entry(root)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ip_entry.insert(0, "192.168.1.1")

        # Port Range Input
        tk.Label(root, text="Start Port:").grid(row=1, column=0, padx=5, pady=5)
        self.start_port_entry = tk.Entry(root)
        self.start_port_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_port_entry.insert(0, "80")

        tk.Label(root, text="End Port:").grid(row=2, column=0, padx=5, pady=5)
        self.end_port_entry = tk.Entry(root)
        self.end_port_entry.grid(row=2, column=1, padx=5, pady=5)
        self.end_port_entry.insert(0, "85")

        # Buttons
        self.scan_button = tk.Button(root, text="Scan Ports", command=self.scan)
        self.scan_button.grid(row=3, column=0, padx=5, pady=5)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear)
        self.clear_button.grid(row=3, column=1, padx=5, pady=5)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Results Display
        self.result_text = tk.Text(root, height=5, width=40)
        self.result_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Treeview Results Table
        self.result_table = ttk.Treeview(root, columns=("Port", "Status"), show="headings")
        self.result_table.heading("Port", text="Port")
        self.result_table.heading("Status", text="Status")
        self.result_table.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Output Directory Label
        self.output_dir_label = tk.Label(root, text=f"Output Directory: {self.output_dir}")
        self.output_dir_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def scan_port(self, ip, port):
        """Scan a single port and return its status."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            return {"port": port, "open": result == 0}
        except socket.gaierror:
            return {"port": port, "open": False, "error": "Invalid IP address"}
        except Exception as e:
            return {"port": port, "open": False, "error": str(e)}

    def scan(self):
        """Initiate the port scan in a background thread."""
        if self.scanning:
            messagebox.showinfo("Info", "Scan already in progress")
            return
        try:
            ip = self.ip_entry.get().strip()
            start_port = int(self.start_port_entry.get())
            end_port = int(self.end_port_entry.get())
            if not ip or start_port > end_port or start_port < 1 or end_port > 65535:
                raise ValueError("Invalid IP or port range (1-65535)")
            socket.inet_aton(ip)  # Validate IP address
            self.scanning = True
            self.scan_button.config(state='disabled')
            self.clear_button.config(state='disabled')
            self.results = []
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Scanning {ip} from {start_port} to {end_port}...\n")
            for item in self.result_table.get_children():
                self.result_table.delete(item)  # Clear table
            self.total_ports = end_port - start_port + 1
            self.progress_bar['maximum'] = self.total_ports
            self.progress_bar['value'] = 0
            thread = threading.Thread(target=self.scan_thread, args=(ip, start_port, end_port))
            thread.start()
            self.check_queue()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            self.scanning = False
            self.scan_button.config(state='normal')
            self.clear_button.config(state='normal')
        except Exception as e:
            messagebox.showerror("Error", f"Scan failed: {e}")
            self.scanning = False
            self.scan_button.config(state='normal')
            self.clear_button.config(state='normal')

    def scan_thread(self, ip, start_port, end_port):
        """Run the scan in a separate thread and queue results."""
        for port in range(start_port, end_port + 1):
            result = self.scan_port(ip, port)
            self.queue.put(result)
        self.queue.put("SCAN_COMPLETE")

    def check_queue(self):
        """Process the queue to update GUI and save results when complete."""
        try:
            while True:
                item = self.queue.get_nowait()
                if item == "SCAN_COMPLETE":
                    self.scanning = False
                    self.scan_button.config(state='normal')
                    self.clear_button.config(state='normal')
                    self.save_results()
                    break
                else:
                    self.results.append(item)
                    status = "open" if item["open"] else "closed"
                    if "error" in item:
                        status += f" ({item['error']})"
                    self.result_text.insert(tk.END, f"Port {item['port']}: {status}\n")
                    self.result_table.insert("", tk.END, values=(item["port"], status))  # Add to Treeview
                    self.progress_bar['value'] += 1
        except queue.Empty:
            pass
        if self.scanning:
            self.root.after(100, self.check_queue)

    def save_results(self):
        """Save scan results to a unique CSV file with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"port_scan_{timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        df = pd.DataFrame(self.results)
        df.to_csv(filepath, index=False)
        self.result_text.insert(tk.END, f"Results saved to {filepath}\n")

    def clear(self):
        """Reset input fields, results, table, and progress bar."""
        self.ip_entry.delete(0, tk.END)
        self.ip_entry.insert(0, "192.168.1.1")
        self.start_port_entry.delete(0, tk.END)
        self.start_port_entry.insert(0, "80")
        self.end_port_entry.delete(0, tk.END)
        self.end_port_entry.insert(0, "85")
        self.result_text.delete(1.0, tk.END)
        for item in self.result_table.get_children():
            self.result_table.delete(item)  # Clear Treeview
        self.results = []
        self.progress_bar['value'] = 0

    def set_output_dir(self):
        """Allow user to set the output directory for CSV files."""
        new_dir = filedialog.askdirectory()
        if new_dir:
            self.output_dir = new_dir
            self.output_dir_label.config(text=f"Output Directory: {self.output_dir}")

    def show_instructions(self):
        """Display usage instructions in a message box."""
        instructions = (
            "Instructions:\n\n"
            "1. Enter the target IP address.\n"
            "2. Enter the start and end port numbers (1-65535).\n"
            "3. Click 'Scan Ports' to start scanning.\n"
            "4. Results will be displayed in the text area and table, and saved to a CSV file.\n"
            "5. Use 'Options' > 'Set Output Directory' to change the save location.\n"
            "6. Click 'Clear' to reset the inputs, results, and table."
        )
        messagebox.showinfo("Instructions", instructions)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = PortScannerGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Failed to start GUI: {e}")
