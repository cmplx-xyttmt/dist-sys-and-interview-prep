"""Step 3 of the L0 rung page (section 2): a file's size versus the disk space it takes.

You write the two functions marked TODO. Then run:

    python3 check.py step3

The check makes a few small files of known sizes, asks your functions about them,
and compares the answers with what `du` (a separate program) says.
"""

import os

# The block size of your Mac's disk. `diskutil info /` prints
# "Allocation Block Size: 4096 Bytes", so a block is 4 KB here.
BLOCK_SIZE = 4096


def blocks_needed(size_bytes):
    """Return how many whole blocks a file of `size_bytes` bytes needs.

    Blocks are never shared between files, and a block is either used or not,
    so a file that is one byte over a block boundary needs a whole extra block.
    An empty file needs no blocks.

    Examples: blocks_needed(1) is 1, blocks_needed(4096) is 1.
    """
    # TODO: your code here (one or two lines)
    raise NotImplementedError("blocks_needed")


def allocated_bytes(path):
    """Return how many bytes of disk the file at `path` takes up.

    Ask the filesystem with os.stat(path). Two fields of the result matter:
    st_size (the length of the file) and st_blocks (how much disk it holds).

    Careful: st_blocks is NOT counted in 4 KB blocks. Run `man 2 stat` in a
    terminal and search for st_blocks (type /st_blocks and press Enter) to find
    the unit it uses.
    """
    # TODO: your code here (one or two lines)
    raise NotImplementedError("allocated_bytes")


if __name__ == "__main__":
    # Try it on the files in this folder before running the check.
    for name in sorted(os.listdir(".")):
        if name.endswith(".py"):
            size = os.stat(name).st_size
            print(f"{name:28} size {size:6} bytes   on disk {allocated_bytes(name):6} bytes"
                  f"   blocks needed {blocks_needed(size)}")
