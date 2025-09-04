#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import time
import os
import random
import itertools

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

# ====== Rotation helpers ======

DEFAULT_UAS = [
    # A small, varied set (you can add more or load from file)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]

def load_lines(path):
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if s and not s.startswith("#"):
                lines.append(s)
    return lines

def cycle_iter(lst):
    return itertools.cycle(lst) if lst else itertools.cycle([None])

def set_proxy_env(proxy_url):
    """
    googlesearch-python does not expose a 'proxies' kwarg.
    We rotate per-request by setting env vars that 'requests' honors.
    """
    if proxy_url:
        os.environ["http_proxy"] = proxy_url
        os.environ["https_proxy"] = proxy_url
    else:
        # Clear proxies for this turn
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)

def jitter(min_s=1.5, max_s=4.0):
    t = random.uniform(min_s, max_s)
    time.sleep(t)

def logger(data):
    """Logs data to a file."""
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(data + "\n")

def dorks():
    """Main function for handling Google Dorking with UA/proxy rotation."""
    global log_file

    try:
        # --- Query + limits ---
        dork = input(f"{Colors.BLUE}\n[+] Enter The Dork Search Query: {Colors.RESET}")

        user_choice = input(f"{Colors.BLUE}[+] Enter Total Number of Results You Want (or type 'all' to fetch everything): {Colors.RESET}").strip().lower()
        if user_choice == "all":
            total_results = float("inf")
        else:
            try:
                total_results = int(user_choice)
                if total_results <= 0:
                    raise ValueError("Number must be greater than zero.")
            except ValueError:
                print(f"{Colors.RED}[ERROR] Invalid number entered! Please enter a positive integer or 'all'.{Colors.RESET}")
                return

        # --- Output settings ---
        save_output = input(f"{Colors.BLUE}\n[+] Do You Want to Save the Output? (Y/N): {Colors.RESET}").strip().lower()
        if save_output == "y":
            log_file_in = input(f"{Colors.BLUE}[+] Enter Output Filename: {Colors.RESET}").strip()
            if log_file_in:
                log_file_in = log_file_in if log_file_in.endswith(".txt") else (log_file_in + ".txt")
                log_file = log_file_in
            else:
                log_file = "dorks_output.txt"

        # --- User-Agent rotation setup ---
        use_ua_file = input(f"{Colors.BLUE}\n[+] Load user-agents from file? (Y/N): {Colors.RESET}").strip().lower() == "y"
        if use_ua_file:
            ua_path = input(f"{Colors.BLUE}[+] Path to user-agents file (one per line): {Colors.RESET}").strip()
            try:
                user_agents = load_lines(ua_path)
                if not user_agents:
                    print(f"{Colors.YELLOW}[!] No UAs found in file. Falling back to defaults.{Colors.RESET}")
                    user_agents = DEFAULT_UAS
            except Exception as e:
                print(f"{Colors.YELLOW}[!] Could not read UA file: {e}. Using defaults.{Colors.RESET}")
                user_agents = DEFAULT_UAS
        else:
            user_agents = DEFAULT_UAS

        ua_cycle = cycle_iter(user_agents)

        # --- Proxy rotation setup ---
        use_proxies = input(f"{Colors.BLUE}\n[+] Use proxies? (Y/N): {Colors.RESET}").strip().lower() == "y"
        proxy_cycle = cycle_iter([None])
        if use_proxies:
            proxy_mode = input(f"{Colors.BLUE}[+] Load proxies from file (F) or enter one now (O)? [F/O]: {Colors.RESET}").strip().lower()
            proxies = []
            if proxy_mode == "f":
                p_path = input(f"{Colors.BLUE}[+] Path to proxies file (one per line, e.g. http://user:pass@host:port or http://host:port): {Colors.RESET}").strip()
                try:
                    proxies = load_lines(p_path)
                except Exception as e:
                    print(f"{Colors.YELLOW}[!] Could not read proxy file: {e}. Continuing without proxies.{Colors.RESET}")
                    proxies = []
            else:
                single = input(f"{Colors.BLUE}[+] Enter a proxy URL (or leave empty to skip): {Colors.RESET}").strip()
                if single:
                    proxies = [single]

            if not proxies:
                print(f"{Colors.YELLOW}[!] No proxies provided. Continuing without proxies.{Colors.RESET}")
                proxy_cycle = cycle_iter([None])
            else:
                proxy_cycle = cycle_iter(proxies)

        # --- Crawl pacing ---
        try:
            min_delay = float(input(f"{Colors.BLUE}\n[+] Min delay between requests (seconds, default 1.5): {Colors.RESET}") or 1.5)
            max_delay = float(input(f"{Colors.BLUE}[+] Max delay between requests (seconds, default 4.0): {Colors.RESET}") or 4.0)
            if max_delay < min_delay:
                min_delay, max_delay = max_delay, min_delay
        except ValueError:
            min_delay, max_delay = 1.5, 4.0

        print(f"\n{Colors.GREEN}[INFO] Searching with UA/proxy rotation... Please wait...{Colors.RESET}\n")

        fetched = 0
        start = 0

        while fetched < total_results:
            # We fetch in chunks (googlesearch-python paginates by start)
            # Keep batch size modest to reduce blocks
            remaining = min(50, total_results - fetched) if total_results != float("inf") else 50

            # Rotate UA and proxy for this batch
            ua = next(ua_cycle)
            px = next(proxy_cycle)
            set_proxy_env(px)

            # Note: googlesearch-python supports 'user_agent' kwarg.
            # Proxies are applied via env vars for 'requests'.
            urls_found = False
            try:
                for result in search(
                    dork,
                    num=remaining,
                    start=start,
                    user_agent=ua,
                ):
                    urls_found = True
                    print(f"{Colors.YELLOW}[+] {Colors.RESET}{result}")
                    if save_output == "y":
                        logger(result)
                    fetched += 1
                    if total_results != float("inf") and fetched >= total_results:
                        break

                    # Per-result jitter
                    time.sleep(random.uniform(min_delay, max_delay))

            except KeyboardInterrupt:
                raise
            except Exception as e:
                # If a proxy gets blocked or fails, report and continue with next rotation
                print(f"{Colors.RED}[ERROR] Batch failed (UA/proxy may be blocked): {e}{Colors.RESET}")

            if not urls_found:
                break  # Stop if no more results are returned

            start += remaining

            # Small pause between batches
            jitter(min_delay, max_delay)

    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] User Interruption Detected! Exiting...{Colors.RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {str(e)}{Colors.RESET}")

    print(f"{Colors.GREEN}\n[✔] Automation Done..{Colors.RESET}")
    sys.exit()

if __name__ == "__main__":
    dorks()
