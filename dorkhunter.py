#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

# Attempt to import the googlesearch module
try:
    from googlesearch import search
except ImportError:
    print("\033[91m[ERROR] Missing dependency: googlesearch-python\033[0m")
    print("\033[93m[INFO] Install it using: pip install googlesearch-python\033[0m")
    sys.exit(1)

# Check for Python version
if sys.version_info[0] < 3:
    print("\n\033[91m[ERROR] This script requires Python 3.x\033[0m\n")
    sys.exit(1)

# ANSI color codes for styling output
class Colors:
    RED = "\033[91m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

# Default output filename
log_file = "dorks_output.txt"

def banner():
    # raw f-string to avoid invalid escape sequence warnings in ASCII art
    print(fr"""{Colors.GREEN}
  ____             _    _   _             _            
 |  _ \  ___  _ __| | _| | | |_   _ _ __ | |_ ___ _ __ 
 | | | |/ _ \| '__| |/ / |_| | | | | '_ \| __/ _ \ '__|
 | |_| | (_) | |  |   <|  _  | |_| | | | | ||  __/ |   
 |____/ \___/|_|  |_|\_\_| |_|\__,_|_| |_|\__\___|_|   
                                                      
{Colors.RESET}""")

def logger(data: str):
    """Logs data to a file."""
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(data + "\n")

def dorks():
    """Main function for handling Google Dorking."""
    global log_file

    try:
        dork = input(f"{Colors.BLUE}\n[+] Enter The Dork Search Query: {Colors.RESET}")

        user_choice = input(
            f"{Colors.BLUE}[+] Enter Total Number of Results You Want (or type 'all' to fetch everything): {Colors.RESET}"
        ).strip().lower()

        if user_choice == "all":
            total_results = float("inf")
            stop_val = None  # googlesearch will keep going until exhausted
        else:
            try:
                total_results = int(user_choice)
                if total_results <= 0:
                    raise ValueError("Number must be greater than zero.")
                stop_val = total_results
            except ValueError:
                print(f"{Colors.RED}[ERROR] Invalid number entered! Please enter a positive integer or 'all'.{Colors.RESET}")
                return

        save_output = input(
            f"{Colors.BLUE}\n[+] Do You Want to Save the Output? (Y/N): {Colors.RESET}"
        ).strip().lower()
        if save_output == "y":
            lf = input(f"{Colors.BLUE}[+] Enter Output Filename: {Colors.RESET}").strip()
            if not lf:
                lf = "dorks_output.txt"
            if not lf.endswith(".txt"):
                lf += ".txt"
            log_file = lf

        print(f"\n{Colors.GREEN}[INFO] Searching... Please wait...{Colors.RESET}\n")

        fetched = 0

        # Use stop to honor user's requested count when provided
        for result in search(dork, num=10, stop=stop_val):
            if total_results != float("inf") and fetched >= total_results:
                break

            print(f"{Colors.YELLOW}[+] {Colors.RESET}{result}")

            if save_output == "y":
                logger(result)

            fetched += 1

        if fetched == 0:
            print(f"{Colors.YELLOW}[!] No results returned.{Colors.RESET}")

    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] User Interruption Detected! Exiting...{Colors.RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {str(e)}{Colors.RESET}")

    print(f"{Colors.GREEN}\n[✔] Automation Done..{Colors.RESET}")
    sys.exit()

if __name__ == "__main__":
    banner()
    dorks()
