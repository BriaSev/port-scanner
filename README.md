Port Scanner for CMMC Compliance Audits
Overview
This Python-based port scanner is designed to identify open network ports for cybersecurity audits, specifically tailored for CMMC (Cybersecurity Maturity Model Certification) compliance. It supports vulnerability assessments by scanning specified IP addresses and port ranges, with results saved in CSV format for analysis. The project includes a command-line version (Port_Scanner.py) and an enhanced GUI version (port_scanner_gui.py) for user-friendly operation.

Features

GUI Scanner (port_scanner_gui.py):
Built with Tkinter for an intuitive user interface.
Allows input of target IP and port range (e.g., 80–85).
Displays real-time scan results in a text area with a progress bar.
Saves each scan to a unique CSV file (e.g., port_scan_2025-05-01_12-30-45.csv) to prevent overwriting.
Includes a "Clear" button to reset inputs and results.
Supports custom output directory selection for CSV files.
Features a Help menu with usage instructions.
Runs scans in a background thread for responsiveness.


Error Handling: Validates IP addresses and port ranges (1–65535), with user-friendly error messages via popups.
Dependencies: Python 3.13.3, pandas, tkinter (included with Python).

Installation

Clone the Repository:git clone https://github.com/BriaSev/port-scanner.git
cd port-scanner


Install Dependencies:pip install pandas

Note: tkinter and socket are included with Python 3.13.3.
Run the Scanner:
Command-line: python Port_Scanner.py
GUI: python port_scanner_gui.py



Usage
Command-Line Scanner

Edit Port_Scanner.py to set the target IP (e.g., 192.168.1.1) and port range (e.g., 80–85).
Run the script to scan and save results to port_scan_results.csv.

GUI Scanner

Launch port_scanner_gui.py.
Enter the target IP (e.g., 192.168.1.1) and port range (e.g., 80–85).
Click "Scan Ports" to start scanning.
View results in the text area and track progress via the bar.
Click "Clear" to reset inputs and results.
Use Options > Set Output Directory to choose where CSVs save.
Check Help > Instructions for guidance.
Results save to a unique CSV (e.g., port_scan_2025-05-01_12-30-45.csv).

Example Output
GUI Output:
Scanning 192.168.1.1 from 80 to 85...
Port 80: open
Port 81: closed
...
Results saved to port_scan_2025-05-01_12-30-45.csv

CSV Output (port_scan_2025-05-01_12-30-45.csv):
port,open
80,True
81,False
...

Project Structure

Port_Scanner.py: Command-line port scanner.
port_scanner_pandas.py: Processes scan results with pandas.
port_scanner_gui.py: Tkinter GUI for user-friendly scanning.
port_scan_*.csv: Generated CSV files with scan results.
Vectors_day1.txt: Notes on vector math for ML applications.

Future Improvements

Add a table view for scan results in the GUI.
Implement multi-threaded scanning for faster performance.
Integrate with ML models for anomaly detection in scan results.

Contributing
Feel free to fork this repository, submit issues, or create pull requests. Contributions to enhance functionality or documentation are welcome!
License
This project is licensed under the MIT License.
Contact
Brian Severson  

LinkedIn: https://www.linkedin.com  
Upwork: https://www.upwork.com/freelancers/~017ed9f2f0beddb52f  
Email: [Your Email]

Built with ❤️ for cybersecurity and compliance.


