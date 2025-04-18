#!/usr/bin/env python2
import sys
import subprocess

def main():
    role = sys.argv[1]

    if role == "sender":
        server_ip = sys.argv[2]
        server_port = sys.argv[3]
        subprocess.check_call(["iperf", "-c", server_ip, "-p", server_port, "-t", "60", "-Z", "reno"])

    elif role == "receiver":
        server_port = sys.argv[2]
        subprocess.check_call(["iperf", "-s", "-p", server_port])

    elif role == "run_first":
        # Choose who runs first. Pantheon prefers "receiver" to go first
        print("receiver")

if __name__ == "__main__":
    main()

