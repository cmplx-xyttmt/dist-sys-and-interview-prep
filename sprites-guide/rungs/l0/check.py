"""Checks for the L0 rung page's do-steps (sprites-guide/l0-a-computer-from-the-inside.html).

    python3 check.py          # every step, one line each
    python3 check.py step3    # one step, with details

Steps: setup, step3, step5, step6, step9 (the numbers match the rung page's steps). Stock python3, nothing to install.
"""

import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True  # keep the folder free of __pycache__
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


class Todo(Exception):
    """A part of the step is not written yet."""


class Fail(Exception):
    """The step is written but something is wrong."""


def load(name):
    try:
        return importlib.import_module(name)
    except SyntaxError as e:
        raise Fail(f"{name}.py has a syntax error on line {e.lineno}: {e.msg}")


def call(fn, *args):
    try:
        return fn(*args)
    except NotImplementedError as e:
        raise Todo(f"{e} is still a TODO")


def expect(got, want, what):
    if got != want:
        raise Fail(f"{what}: expected {want!r}, got {got!r}")


# ------------------------------------------------------------------ setup
def check_setup(say):
    say(f"python3 {sys.version.split()[0]}: fine")
    if shutil.which("docker") is None:
        raise Fail("no `docker` command found. Steps 6 and 9 need Docker Desktop.")
    r = subprocess.run(["docker", "info"], capture_output=True, text=True)
    if r.returncode != 0:
        raise Fail("Docker is installed but not running yet. Run `open -a Docker`; it takes "
                   "a minute to start, and you don't need it until step 6.")
    say("Docker Desktop is running")


# ------------------------------------------------------------------ step 3
def du_bytes(path):
    out = subprocess.run(["du", "-k", path], capture_output=True, text=True, check=True).stdout
    return int(out.split()[0]) * 1024


def check_step3(say):
    m = load("step3_blocks")
    for size, want in [(0, 0), (1, 1), (4095, 1), (4096, 1), (4097, 2), (10000, 3), (8192, 2)]:
        expect(call(m.blocks_needed, size), want, f"blocks_needed({size})")
    say("blocks_needed: right on 7 sizes")

    rows = []
    with tempfile.TemporaryDirectory(dir=HERE) as d:
        for size in [0, 1, 4096, 4097, 10000]:
            p = os.path.join(d, f"file-{size}")
            with open(p, "w") as f:
                f.write("a" * size)
            got = call(m.allocated_bytes, p)
            du = du_bytes(p)
            if got != du:
                hint = ""
                if du and got * 8 == du:
                    hint = " (off by a factor of 8: check the unit of st_blocks)"
                elif du and got == du * 8:
                    hint = " (8 times too big: st_blocks is not in 4 KB blocks)"
                raise Fail(f"allocated_bytes for a {size}-byte file: `du` says {du}, you said {got}{hint}")
            rows.append((size, got, m.blocks_needed(size)))
    say("allocated_bytes: matches `du` on 5 real files")
    say("")
    say("   size   on disk   blocks")
    for size, got, b in rows:
        say(f"  {size:5}   {got:7}   {b:6}")
    say("")
    say("A 1-byte file takes a whole 4096-byte block, and 4097 bytes take two.")


# ------------------------------------------------------------------ step 5 (inode)
def check_step5(say):
    m = load("step5_inode")
    cases = [  # inumber, byte address, block, sector
        (0, 12288, 3, 24),
        (1, 12544, 3, 24),
        (15, 16128, 3, 31),
        (16, 16384, 4, 32),
        (32, 20480, 5, 40),
        (34, 20992, 5, 41),
        (79, 32512, 7, 63),
    ]
    for i, addr, _, _ in cases:
        expect(call(m.inode_byte_address, i), addr, f"inode_byte_address({i})")
    say("inode_byte_address: right on 7 inodes")
    for bad in (80, -1):
        try:
            call(m.inode_byte_address, bad)
        except ValueError:
            continue
        raise Fail(f"inode_byte_address({bad}) should raise ValueError (only inodes 0 to 79 exist)")
    say("inode_byte_address: rejects 80 and -1")
    for i, _, blk, _ in cases:
        expect(call(m.inode_block, i), blk, f"inode_block({i})")
    say("inode_block: right on 7 inodes")
    for i, _, _, sec in cases:
        expect(call(m.inode_sector, i), sec, f"inode_sector({i})")
    say("inode_sector: right on 7 inodes")
    say("")
    say("Inodes 0 to 15 share block 3, so reading any one of them fetches all sixteen.")


# ------------------------------------------------------------------ step 6
def check_step6(say):
    m = load("step6_timing")
    path = os.path.join(HERE, "timings.json")
    if not os.path.exists(path):
        if m.PREDICTED_PULL_SECONDS is None or m.PREDICTED_RUN_SECONDS is None:
            raise Todo("predictions in step6_timing.py are still None; write them, then run "
                       "`python3 run_timing.py`")
        raise Todo("no timings.json yet: run `python3 run_timing.py`")
    say("predictions written and timings.json measured")

    for xs, want in [([3, 1, 2], 2), ([5], 5), ([4, 1, 3, 2], 2.5), ([0.9, 0.7, 5.0], 0.9)]:
        given = list(xs)
        expect(call(m.median, given), want, f"median({xs})")
        expect(given, xs, "median changed the list it was given")
    say("median: right on 4 lists, input left alone")
    with open(path) as f:
        t = json.load(f)
    run_med = m.median(t["run_seconds"])
    pred_ratio = t["predicted_pull_seconds"] / t["predicted_run_seconds"]
    real_ratio = t["pull_seconds"] / run_med
    say("")
    say("            predicted   measured")
    say(f"  pull      {t['predicted_pull_seconds']:8.1f} s {t['pull_seconds']:8.1f} s")
    say(f"  run       {t['predicted_run_seconds']:8.2f} s {run_med:8.2f} s   (median of "
        + ", ".join(f"{x:.2f}" for x in t["run_seconds"]) + ")")
    say(f"  ratio     {pred_ratio:8.1f}   {real_ratio:8.1f}")
    say("")
    off = max(pred_ratio / real_ratio, real_ratio / pred_ratio)
    if off <= 3:
        say(f"Your ratio was within {off:.1f}x of the measured one.")
    elif m.SURPRISE.strip():
        say(f"Off by {off:.1f}x, and you wrote down why: \"{m.SURPRISE.strip()}\"")
    else:
        raise Fail(f"your ratio is off by {off:.1f}x. Write one sentence in SURPRISE in "
                   "step6_timing.py on what you had wrong, then run the check again.")


# ------------------------------------------------------------------ step 9
def check_step9(say):
    m = load("step9_inside_outside")
    blank = [k for k, v in m.PREDICT.items() if v not in ("same", "different")]
    if blank or m.PREDICT_VM_SEES_CONTAINER_SLEEP not in (True, False):
        raise Todo("fill in every prediction in step9_inside_outside.py "
                   "(\"same\"/\"different\", and True/False), then run `python3 run_compare.py`")
    path = os.path.join(HERE, "compare.json")
    if not os.path.exists(path):
        raise Todo("no compare.json yet: run `python3 run_compare.py`")
    with open(path) as f:
        c = json.load(f)

    wrong = []
    say("")
    say("  command            you said    measured")
    for cmd, r in c["results"].items():
        real = "same" if r["vm"] == r["container"] else "different"
        said = c["predict"][cmd]
        mark = "" if said == real else "   <- wrong"
        if said != real:
            wrong.append(cmd)
        say(f"  {cmd:18} {said:10}  {real:10}{mark}")
    seen = bool(c["vm_ps_lines_for_sleep"].strip())
    said = c["predict_vm_sees_container_sleep"]
    mark = "" if said == seen else "   <- wrong"
    if said != seen:
        wrong.append("the sleep process")
    say(f"  {'VM sees sleep 300':18} {str(said):10}  {str(seen):10}{mark}")
    say("")
    kr = c["results"].get("uname -r", {})
    if kr:
        say(f"Kernel version: container {kr.get('container')!r}, Linux VM {kr.get('vm')!r}, "
            f"your Mac {kr.get('mac')!r}.")
    if not wrong:
        say("Every prediction right.")
    elif m.NOTES.strip():
        say(f"{len(wrong)} wrong, and your NOTES explain them.")
    else:
        raise Fail(f"{len(wrong)} prediction(s) wrong ({', '.join(wrong)}). Write one sentence "
                   "for each in NOTES in step9_inside_outside.py, then run the check again.")


STEPS = {
    "setup": check_setup,
    "step3": check_step3,
    "step5": check_step5,
    "step6": check_step6,
    "step9": check_step9,
}


def run_one(name, verbose):
    lines = []
    say = lines.append
    try:
        STEPS[name](say)
        status, why = "PASS", ""
    except Todo as e:
        status, why = "TODO", str(e)
    except Fail as e:
        status, why = "FAIL", str(e)
    except Exception as e:  # a bug in the step's code, not in the check
        status, why = "FAIL", f"your code raised {type(e).__name__}: {e}"
    if verbose:
        for line in lines:
            print("  " + line if line else "")
        print(f"{name}: {status}" + (f": {why}" if why else ""))
    else:
        print(f"{name:6} {status}" + (f"  {why}" if why else ""))
    return status == "PASS"


def main():
    args = sys.argv[1:]
    if not args:
        results = [run_one(n, verbose=False) for n in STEPS]
        print(f"\n{sum(results)} of {len(results)} passing. "
              "`python3 check.py step3` shows one step in detail.")
        sys.exit(0 if all(results) else 1)
    for a in args:
        if a not in STEPS:
            print(f"Unknown step {a!r}. Choose from: {', '.join(STEPS)}")
            sys.exit(2)
    ok = all(run_one(a, verbose=True) for a in args)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
