"""Run the same commands on your Mac, in Docker Desktop's Linux VM, and in a container.
Plumbing for step 7: you don't edit this.

    python3 run_compare.py

Refuses to start until every prediction in step7_inside_outside.py is filled in.
Writes compare.json next to this file and prints a table.

How it reaches the Linux VM: `docker run --privileged --pid=host alpine nsenter -t 1 ...`
starts a tiny container that is allowed to see every process on the VM, then
`nsenter` joins the namespaces of process 1 (the VM's first process). From there
the shell sees what the VM sees. This is the command from the L0 page's mission.
"""

import json
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True

import step7_inside_outside as mine
from run_timing import docker_ready

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "compare.json")
IMAGE = os.environ.get("L0_IMAGE", "python:3.12")  # override only for testing

VM = ["docker", "run", "--rm", "--privileged", "--pid=host", "alpine",
      "nsenter", "-t", "1", "-m", "-u", "-n", "-i", "sh", "-c"]
CONTAINER = ["docker", "run", "--rm", IMAGE, "sh", "-c"]
SLEEPER = "l0-sleeper"


def run(prefix, cmd):
    r = subprocess.run(prefix + [cmd], capture_output=True, text=True)
    out = r.stdout.strip()
    if r.returncode != 0 and not out:
        out = "(error) " + r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "(error)"
    return out


def main():
    missing = [k for k, v in mine.PREDICT.items() if v not in ("same", "different")]
    if missing or mine.PREDICT_VM_SEES_CONTAINER_SLEEP not in (True, False):
        print("Fill in every prediction in step7_inside_outside.py first:")
        for k in missing:
            print(f'  PREDICT["{k}"] should be "same" or "different"')
        if mine.PREDICT_VM_SEES_CONTAINER_SLEEP not in (True, False):
            print("  PREDICT_VM_SEES_CONTAINER_SLEEP should be True or False")
        sys.exit(1)
    if not docker_ready():
        sys.exit(1)

    results = {}
    for cmd in mine.PREDICT:
        print(f"running `{cmd}` in three places...")
        results[cmd] = {
            "mac": run(["sh", "-c"], cmd),
            "vm": run(VM, cmd),
            "container": run(CONTAINER, cmd),
        }

    print("starting a container that runs `sleep 300`, then looking for it from the VM...")
    subprocess.run(["docker", "rm", "-f", SLEEPER], capture_output=True)
    subprocess.run(["docker", "run", "-d", "--rm", "--name", SLEEPER, "alpine", "sleep", "300"],
                   capture_output=True, check=True)
    time.sleep(1)
    seen = run(VM, "ps aux | grep '[s]leep 300'")
    subprocess.run(["docker", "rm", "-f", SLEEPER], capture_output=True)

    record = {
        "image": IMAGE,
        "predict": mine.PREDICT,
        "predict_vm_sees_container_sleep": mine.PREDICT_VM_SEES_CONTAINER_SLEEP,
        "results": results,
        "vm_ps_lines_for_sleep": seen,
        "measured_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(OUT, "w") as f:
        json.dump(record, f, indent=2)

    for cmd, r in results.items():
        print(f"\n$ {cmd}")
        for where in ("mac", "vm", "container"):
            first = r[where].splitlines()
            shown = " / ".join(first[:4]) + (" ..." if len(first) > 4 else "")
            print(f"  {where:10} {shown or '(nothing)'}")
    print("\nThe VM's process list, filtered for `sleep 300`:")
    print("  " + (seen or "(nothing)"))
    print(f"\nSaved {os.path.basename(OUT)}. Next: `python3 check.py step7`.")


if __name__ == "__main__":
    main()
