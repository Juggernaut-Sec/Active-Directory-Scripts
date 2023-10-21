#!/usr/bin/env python3

#SMB Share Name Brute Forcer Script
#Supply an RHOST and a wordlist to start brute forcing
#Manually edit threading below to make the script run faster

import sys
import subprocess
import threading

if len(sys.argv) != 3:
    print("Usage: {} <RHOST> <wordlist>".format(sys.argv[0]))
    sys.exit(1)

RHOST = sys.argv[1]
wordlist = sys.argv[2]

# Create a lock to synchronize printing
print_lock = threading.Lock()

def check_share(word):
    smb_process = subprocess.Popen(['smbclient', f'//{RHOST}/{word}', '-N'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = smb_process.communicate()

    if "NT_STATUS_ACCESS_DENIED" in stdout.decode():
        with print_lock:
            print("[+] Share Found --> {}".format(word))
    elif smb_process.returncode == 0:
        with print_lock:
            print("[+] Share Found --> {} --> Anonymous Access Granted!".format(word))

try:
    with open(wordlist, 'r') as fh:
        words = [line.strip() for line in fh]

    # Define the number of threads to use
    num_threads = 20

    # Create and start threads
    threads = []
    for i in range(0, len(words), num_threads):
        thread_words = words[i:i + num_threads]
        for word in thread_words:
            thread = threading.Thread(target=check_share, args=(word,))
            thread.start()
            threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

except FileNotFoundError:
    print("Error: Wordlist file not found.")
except Exception as e:
    print("An error occurred: {}".format(e))
