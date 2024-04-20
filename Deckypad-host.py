#!/usr/bin/env python
import sys, os, re, time
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/class/")

import Network
Net = Network.Manage()
import signal
import threading
client_threads = []

def signal_handler(sig, frame):
    print('\n\nYou pressed Ctrl+C\nDeckypad has stopped')
    os._exit(0)

def _help():
    print("This is the host side of Deckypad")
    print("----------------------------------")
    print("Usage:  python3 Deckypad-host.py <Port Number> <Host interface IP>")
    print("Arguments are optional - defaults are\n PORT: 9090\n Host: 0.0.0.0")
    sys.exit(0)


def main():
    print("Running Deckypad on "+str(Net.HOST)+":"+str(Net.PORT))
    print('\nSend SIGINT or Press Ctrl+C at anytime to quit')
    signal.signal(signal.SIGINT, signal_handler)
    if Net.start_host():
        while True:
            if not Net.queue.empty():
                item = Net.queue.get()
                client_thread = threading.Thread(target=Net.server_newclient, args=[item[0],item[1]])
                client_threads.append(client_thread)
                client_thread.start()
                print("Client joined")
            else:
                time.sleep(1)
    else:
        print("\n * Failed to start server ")



if __name__ == "__main__":
    help = ["-h", "-?", "/?", "/h", "--help", "-help", "help"]
    if len(sys.argv) > 3:
        _help()
    else:
        for x in sys.argv:
            if x in help:
                _help()
    if len(sys.argv) >= 2:
        port_regex = "^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
        if not re.search(port_regex, sys.argv[1]):
            print("invalid port number\n")
            _help()
        else:
            Net.PORT = sys.argv[1]
    if len(sys.argv) >= 3:
        print("has ip")
        ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if not re.search(ip_regex, sys.argv[2]):
            print("invalid IP\n")
            _help()
        else:
            Net.HOST = sys.argv[2]
    main()
