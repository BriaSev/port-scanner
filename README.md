Port Scanner with Tkinter GUI
A Python-based port scanner with a Tkinter GUI, designed for cybersecurity professionals to perform network audits, including support for CMMC compliance. Features a user-friendly interface with a results table, CSV output, and customizable settings.
Features

Graphical Interface: Built with Tkinter, featuring input fields for target IP and port range, a progress bar, and a Treeview table for real-time port status display.
Port Scanning: Scans TCP ports using the socket library, with threading for efficient performance.
Results Display: Shows open/closed ports in both a text area and a Treeview table, with error handling for invalid inputs.
CSV Export: Saves scan results to timestamped CSV files using pandas, with customizable output directory.
User Controls: Includes "Scan Ports", "Clear", and "Set Output Directory" options, plus a help menu with instructions.
CMMC Support: Useful for network audits in CMMC Level 1 compliance, identifying open ports for scoping assessments.


Requirements

Python 3.13.3 or later
Libraries: tkinter, pandas
Install pandas: pip install pandas



Installation

Clone the repository:git clone https://github.com/BriaSev/port-scanner.git
cd port-scanner


Install dependencies:pip install pandas


Run the scanner:python port_scanner_gui_1.1.py



Usage

Launch the application: python port_scanner_gui_1.1.py
Enter the target IP (e.g., 127.0.0.1) and port range (e.g., 80-85).
Click Scan Ports to start scanning.
View results in the text area and Treeview table.
Results are saved as a CSV (e.g., port_scan_2025-05-03_14-30-45.csv) in the chosen directory.
Use Options > Set Output Directory to change the save location.
Click Clear to reset inputs and results.
Access Help > Instructions for guidance.

Files

port_scanner_gui_1.1.py: Main GUI application with Treeview table, progress bar, and CSV output.
gui_table_output_20250503.png: Screenshot of the GUI with results table.

Contributing
Contributions are welcome! Please submit a pull request or open an issue for bugs or feature requests.
License
MIT License
Author
Brian Severson - CMMC Consultant & Python Developer

LinkedIn: https://www.linkedin.com
Upwork: https://www.upwork.com/freelancers/~017ed9f2f0beddb52f

