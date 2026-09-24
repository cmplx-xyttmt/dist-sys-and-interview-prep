"""Step 5 of the L0 rung page (section 2): find an inode on the disk.

The OSTEP chapter builds a tiny example filesystem (it calls it "vsfs") on a
disk of 64 blocks. The numbers below are the ones from the chapter's pictures.
Check each one against the figure before you start: if one looks wrong to you,
trust the chapter and fix it here.

You write the three functions marked TODO. Then run:

    python3 check.py step5
"""

BLOCK_SIZE = 4096          # bytes per block
SECTOR_SIZE = 512          # bytes per disk sector (the unit the disk itself reads)
INODE_SIZE = 256           # bytes per inode
INODE_TABLE_START = 12 * 1024   # byte address where the inode table begins
NUM_INODES = 80            # inodes 0 to 79 exist; anything else is an error


def inode_byte_address(inumber):
    """Return the byte address on disk where inode number `inumber` starts.

    Raise ValueError if `inumber` is not a valid inode number.
    The chapter works one example out in full: inode 32 starts at 20 KB.
    """
    # TODO: your code here
    raise NotImplementedError("inode_byte_address")


def inode_block(inumber):
    """Return the number of the disk block that holds inode `inumber`.

    Block 0 is the first block of the disk (the superblock), block 1 the next,
    and so on. The filesystem can only read whole blocks, so this is the block
    it has to fetch to look at the inode.
    """
    # TODO: your code here (reuse inode_byte_address)
    raise NotImplementedError("inode_block")


def inode_sector(inumber):
    """Return the number of the sector that holds the first byte of inode `inumber`.

    Sector 0 is the first 512 bytes of the disk, sector 1 the next 512, and so on.
    """
    # TODO: your code here (reuse inode_byte_address)
    raise NotImplementedError("inode_sector")


if __name__ == "__main__":
    for i in (0, 16, 32, 79):
        print(f"inode {i:2}: byte {inode_byte_address(i):6}, "
              f"block {inode_block(i)}, sector {inode_sector(i)}")
