#!/usr/bin/python3

import argparse
import os
import platform
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument(
    "--id", "-i", type=str, default="", help="`.mdp<id>` file name, default is ''"
)

parser.add_argument("--base-path", "-p", type=str, default="~/", help="`/base/path/.mdp<id>` file name, default base path is home")

parser.add_argument("--ssh-config", "-s", type=str, default=str(Path.home())+ "/.ssh/config", help="Path to your ssh config, default is ~/.ssh/config")

parser.add_argument("--clipboard-util", "-u", type=str, default="xclip -selection c" if platform.system() == "Linux" else "pbcopy", help="Clipboard utility to use, default is `xclip -selection c` on nux and `pbclip` on macos")

parser.add_argument("--output", "-o", type=bool, default=False, nargs="?", const=True, help="Prints the password instead of putting it to clipboard")

parser.add_argument("--verbose", "-v", type=bool, default=False, nargs="?", const=True)



args = parser.parse_args()

ID = args.id
VERBOSE = args.verbose
REMOTE_BASE_PATH=args.base_path
SSH_CONFIG = args.ssh_config
CLIPPING_UTIL = args.clipboard_util
CLIP_OUTPUT = not args.output


if not os.path.exists(str(Path.home())):
    print("No ssh config not found: `f{SSH_CONFIG}`")
    exit(1)

def get_hosts():
    config = open(SSH_CONFIG,"r")
    content = config.read()
    hostnames = []
    for line in content.split("\n"):
        line = line.strip()
        takeNext = False
        for word in line.split(" "):
            word = word.strip()
            if word == "":
                continue
            if takeNext:
                hostnames.append(word)
            if word == "Host":
                takeNext = True
    config.close()
    return hostnames

hosts = get_hosts()

if VERBOSE:
    print("Hosts:", hosts)

for host in hosts:
    if VERBOSE:
        print(f"Contacting host {host}...")

    proc = subprocess.Popen(
        [f"ssh -o LogLevel=QUIET -t {host} 'cat {REMOTE_BASE_PATH}.mdp{ID}' "],
        stdout=subprocess.PIPE,
        shell=True,
    )
    (mdp, _) = proc.communicate()

    if proc.returncode == 0:
        if CLIP_OUTPUT:
            ret = os.system(f"echo {mdp} | tr -d '\n' | tr -d '\r' | {CLIPPING_UTIL}")
            if ret == 0:
                if VERBOSE:
                    print("Clipped!")
                exit(0)
        else:
            ret = os.system(f"echo {mdp} | tr -d '\n' | tr -d '\r'")
            if ret == 0:
                exit(0)

    elif VERBOSE:
        print("Error:", mdp)

exit(1)
