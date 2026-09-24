"""Step 9 of the L0 rung page (section 2): inside a container versus the Linux machine it runs on.

On a Mac, "the machine the container runs on" is not macOS. Docker Desktop runs
a hidden Linux virtual machine, and every container is a process inside it.
run_compare.py runs each command below in three places: your Mac, that Linux VM,
and a python:3.12 container.

1. Fill in every prediction below BEFORE running anything.
   For each command: will the container print the "same" output as the Linux VM,
   or "different" output?
2. Run `python3 run_compare.py`. It copies your predictions into compare.json.
3. Run `python3 check.py step9`. It shows which predictions were wrong.
4. For each wrong one, write a sentence in NOTES, and run the check again.
"""

# TODO: "same" or "different" for each command (container compared with the Linux VM).
PREDICT = {
    "hostname": None,          # the machine's name
    "uname -r": None,          # the kernel's version
    "ls /proc | head": None,   # the first entries of the kernel's live view of processes
    "mount | wc -l": None,     # how many filesystems are mounted
    "ps aux | wc -l": None,    # how many processes are visible (plus one header line)
}

# TODO: True or False. A container runs `sleep 300`. From the Linux VM's shell,
# can `ps aux` see that sleep process?
PREDICT_VM_SEES_CONTAINER_SLEEP = None

# TODO, after the check: one sentence for each prediction you got wrong.
NOTES = ""
