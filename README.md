# 🔎 DorkHunter

![Python](https://img.shields.io/badge/python-3.x-blue.svg) 
![License](https://img.shields.io/badge/license-MIT-green.svg) 
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)




## 📖 About
**DorkHunter** is a Python-based tool that automates **Google Dorking** queries.  
It helps penetration testers, bug bounty hunters, and security researchers quickly gather search results with optional output logging.  

⚠️ **Disclaimer:** Use this tool only for **ethical security testing**.  
The author is **not responsible** for any misuse.  

---

## ✨ Features
- Run **custom Google dork queries**  
- Fetch a **specific number of results** or **all available results**  
- Option to **save output to a file** (`.txt`)  
- **Color-coded output** for readability  
- Handles **CTRL+C** gracefully  

---

## 🚀 Installation
```bash

git clone https://github.com/HARZE12/DorkHunter.git
cd DorkHunter
```
# Install required dependency
```
pip install googlesearch-python
```
⚡ Usage
```
python3 dorkhunter.py
```

📂 Example Run
```
[+] Enter The Dork Search Query: site:example.com inurl:login
[+] Enter Total Number of Results You Want (or type 'all' to fetch everything): 50
[+] Do You Want to Save the Output? (Y/N): y
[+] Enter Output Filename: example_dorks.txt

[INFO] Searching... Please wait...

[+] https://example.com/login.php
[+] https://example.com/admin/
[+] https://portal.example.com/auth

[✔] Automation Done..
```

Results saved to example_dorks.txt ✅


#📜 Legal Disclaimer

This project is intended for educational and authorized penetration testing only.
Do not use it against systems without explicit permission.
The user is fully responsible for compliance with applicable laws.

