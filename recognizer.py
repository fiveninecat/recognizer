import argparse
from datetime import datetime
import json
import os
import socket
import sys

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

parser = argparse.ArgumentParser(description="scan a target for open tcp ports and return banners if available")
parser.add_argument("target", help="target to scan")
parser.add_argument("-t", "--timeout", type=check_positive, default=5, help="set timeout")
parser.add_argument("-s", "--save", action="store_true", help="output scan results to a json file")
args = parser.parse_args()

# set title
title = "recognizer.py"
version = "1.0.0"

# create dictionary to save scan info
scan_info = {
    "target": {},
    "timeout": None,
    "timestamps": {},
    "open_ports": [],
    "banners": {}
}

# start saving scan info

scan_info["target"]["user_input"] = args.target
scan_info["target"]["target_ip"] = socket.gethostbyname(args.target)
scan_info["timeout"] = args.timeout

# print program title and basic scan info for the user

print(f"{title} v{version}")

print("scanning target {} {}".format(scan_info["target"]["user_input"], scan_info["target"]["target_ip"]))

t = scan_info["timeout"]
print(f"timeout set to {t} second") if t == 1 else print(f"timeout set to {t} seconds")

# save starting timestamps

started = datetime.now()

started_simple = started.strftime("%Y%m%d%H%M%S")
scan_info["timestamps"]["started_simple"] = started_simple

started_readable = started.strftime("%Y-%m-%d %H:%M:%S")
scan_info["timestamps"]["started_readable"] = started_readable

# print scan start time

print("scan started: {}".format(scan_info["timestamps"]["started_readable"]))

# run scan

for port in range(1,65536):

    # create a socket and set timeout
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set timeout value
    s.settimeout(scan_info["timeout"])

    # try to connect to port
    try:
        s.connect((scan_info["target"]["target_ip"], port))

    # if unsuccessful
    except:

        # move on to next port
        continue

    # if successful
    else:

        # save port number
        scan_info["open_ports"].append(port)

        # try to get banner
        try: 
            banner = s.recv(1024).decode()

        # if unsuccessful
        except:

            # print open port number
            print("{}".format(port))

        # if successful
        else:

            # save banner
            scan_info["banners"][port] = banner

            # print open port number and banner
            print("{} {}".format(port, scan_info["banners"][port]))

    # close connection
    finally:
        s.close()

# save ending timestamps

completed = datetime.now()

completed_simple = completed.strftime("%Y%m%d%H%M%S")
scan_info["timestamps"]["completed_simple"] = completed_simple

completed_readable = completed.strftime("%Y-%m-%d %H:%M:%S")
scan_info["timestamps"]["completed_readable"] = completed_readable

# print scan end time

print("scan completed: {}".format(scan_info["timestamps"]["completed_readable"]))

# if the -s or --save flag has been set, save scan results

if args.save:

    save_dir = os.path.expanduser("~/.recognizer_scans")

    # if save_dir does not exist
    if not os.path.exists(save_dir):
        
        # print a message
        print("{} does not exist, trying to create it now".format(save_dir))

        # try to create save_dir
        try:
            os.mkdir(save_dir)

        # if unsuccessful, print a message and exit
        except:
            print(f"could not create {save_dir} so unable to save scan")
            sys.exit()

        # if successful, print a message
        else:
            print(f"success, created {save_dir}")

    # create a filename for the saved scan using simple timestamps created earlier
    save_file = f"{save_dir}/scan_{started_simple}_{completed_simple}.json"

    # try to save scan results in json format and print a status message
    try:
        with open(f"{save_file}", "w") as output_file:
            json.dump(scan_info, output_file)
    except:
        print("unable to save scan")
    else:
        print(f"scan saved to {save_file}")
