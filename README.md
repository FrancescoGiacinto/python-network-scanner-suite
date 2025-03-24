### Python for Cybersecurity – PRE-ATT&CK Tools
This repository contains a collection of Python scripts inspired by the "Python for Cybersecurity Specialization" course by Howard Poston on Coursera.
The focus is on implementing reconnaissance techniques aligned with the MITRE ATT&CK PRE-ATT&CK phase.

These scripts are educational in nature and showcase how Python can be used for scanning, enumeration, and automation during the initial stages of a cybersecurity assessment.

⚠️ Disclaimer
⚠️ This project is intended for educational purposes only.

The scripts in this repository demonstrate techniques such as DNS scanning, TCP port scanning, and subdomain enumeration.

Do not run these scripts against domains, networks, or systems that you do not own or do not have explicit written permission to test.

Unauthorized scanning may be considered illegal or unethical depending on your jurisdiction and the target.

The author is not responsible for any misuse or unauthorized use of this code.

Always test responsibly, ethically, and with proper consent.

### About the Scripts
These scripts are based on demonstrations from the "Python for Cybersecurity Specialization" by Howard Poston.

They have been transcribed and adapted for Windows users, where necessary.

While the original logic follows the course content, I may modify, improve, or expand these tools over time for learning and portfolio purposes.

### Dependencies
Install the required Python libraries:


pip install python-nmap dnspython

Library	Purpose
python-nmap	Interface to run and parse Nmap scans via Python
dnspython	Perform DNS queries directly from Python scripts

### On Windows
Make sure Nmap is installed and added to your system PATH.

