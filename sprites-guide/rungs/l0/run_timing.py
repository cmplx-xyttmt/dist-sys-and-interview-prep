"""Measure a container pull and a container start. Plumbing for step 5: you don't edit this.

    python3 run_timing.py              # remove the image, time the pull, time 3 runs
    python3 run_timing.py --runs-only  # keep the pull time you already have, re-time the runs

Refuses to start until the predictions in step5_timing.py are filled in.
Writes timings.json next to this file.
"""

import json
import os
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True

import step5_timing

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "timings.json")
IMAGE = os.environ.get("L0_IMAGE", "python:3.12")  # override only for testing
RUN_CMD = ["docker", "run", "--rm", IMAGE, "python", "-c", "print(1)"]
if IMAGE != "python:3.12":
    RUN_CMD = ["docker", "run", "--rm", IMAGE, "echo", "1"]


def docker_ready():
    if shutil.which("docker") is None:
        print("No `docker` command found. Is Docker Desktop installed?")
        return False
    r = subprocess.run(["docker", "info"], capture_output=True, text=True)
    if r.returncode != 0:
        print("Docker is installed but not running. Run `open -a Docker`, wait until")
        print("the whale icon in the menu bar stops animating, and try again.")
        return False
    return True


def timed(cmd, show_output):
    start = time.perf_counter()
    r = subprocess.run(cmd, capture_output=not show_output, text=True)
    elapsed = time.perf_counter() - start
    if r.returncode != 0:
        print(f"`{' '.join(cmd)}` failed.")
        if not show_output:
            print(r.stderr)
        sys.exit(1)
    return elapsed


def main():
    pull_p = step5_timing.PREDICTED_PULL_SECONDS
    run_p = step5_timing.PREDICTED_RUN_SECONDS
    if pull_p is None or run_p is None:
        print("Write your two predictions in step5_timing.py first. That is the mission:")
        print("the guess has to exist before the measurement does.")
        sys.exit(1)
    if not docker_ready():
        sys.exit(1)

    runs_only = "--runs-only" in sys.argv
    old = {}
    if runs_only:
        if not os.path.exists(OUT):
            print("--runs-only needs an earlier timings.json. Run without it first.")
            sys.exit(1)
        with open(OUT) as f:
            old = json.load(f)
        pull_s = old["pull_seconds"]
        print(f"Keeping the earlier pull time: {pull_s:.1f} s")
    else:
        have = subprocess.run(["docker", "image", "inspect", IMAGE], capture_output=True)
        if have.returncode == 0:
            print(f"Removing your local {IMAGE} so the pull starts from nothing...")
            rm = subprocess.run(["docker", "rmi", IMAGE], capture_output=True, text=True)
            if rm.returncode != 0:
                print(rm.stderr)
                print("Could not remove it (a stopped container may still use it;")
                print("`docker ps -a` lists them, `docker rm <id>` removes one). Then try again.")
                sys.exit(1)
        print(f"\nTiming `docker pull {IMAGE}`. Docker's own progress output follows.")
        print("This can take a few minutes. Start step 6's reading while it runs.\n")
        pull_s = timed(["docker", "pull", IMAGE], show_output=True)
        print(f"\npull: {pull_s:.1f} s")

    runs = []
    for i in range(3):
        s = timed(RUN_CMD, show_output=False)
        runs.append(s)
        print(f"run {i + 1}: {s:.2f} s")

    record = {
        "image": IMAGE,
        "predicted_pull_seconds": old.get("predicted_pull_seconds", pull_p),
        "predicted_run_seconds": old.get("predicted_run_seconds", run_p),
        "pull_seconds": pull_s,
        "run_seconds": runs,
        "measured_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(OUT, "w") as f:
        json.dump(record, f, indent=2)
    print(f"\nSaved {os.path.basename(OUT)}. Next: write median() in step5_timing.py,")
    print("then run `python3 check.py step5`.")


if __name__ == "__main__":
    main()
