# CLI utility to fetch passwords on remote hosts

The utility scans your ssh config then contact each hosts looking for file `/base/path/.mdp<id>` containing your password on the remote host:

- `/base/path` is set with `--base-path` argument, default is home
- `<id>` is set with `--id` argument, default is '', i.e. the file name is `.mdp`

If an host answers positively the script copies the password in your clipboard (or outputs it if `-o`).

## Install

You need `python3` on your system (tested on `>= 3.8` but probably works with earlier versions too).

If you want a systemwide installation of `mdp` do:

`./install.sh`

## Usage

```
usage: mdp.py [-h] [--id ID] [--base-path BASE_PATH] [--ssh-config SSH_CONFIG]
              [--clipboard-util CLIPBOARD_UTIL] [--output [OUTPUT]]
              [--verbose [VERBOSE]]

optional arguments:
  -h, --help            show this help message and exit
  --id ID, -i ID        Identifier resulting in `.mdp<id>` file name, default
                        is ''
  --base-path BASE_PATH, -p BASE_PATH
                        Look for `/base/path/.mdp` on remote host, default is
                        home
  --ssh-config SSH_CONFIG, -s SSH_CONFIG
                        Path to your ssh config, default is ~/.ssh/config
  --clipboard-util CLIPBOARD_UTIL, -u CLIPBOARD_UTIL
                        Clipboard utility to use, default is `xclip -selection
                        c` on nux and `pbclip` on macos
  --output [OUTPUT], -o [OUTPUT]
                        Prints the password instead of putting it to clipboard
  --verbose [VERBOSE], -v [VERBOSE]
```