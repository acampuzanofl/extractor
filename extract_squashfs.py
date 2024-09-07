#!/usr/bin/python3

import struct

# Constants for SquashFS signature and superblock
SQUASHFS_MAGIC = 0x73717368  # Magic number for SquashFS
SUPERBLOCK_SIZE = 96  # Size of SquashFS superblock

def extract_squashfs_partitions(input_file, output_prefix):
    with open(input_file, 'rb') as f:
        # Read the entire binary blob
        data = f.read()

    # Initialize partition counter
    partition_count = 0
    offset = 0

    # Scan the entire file without assuming partitions' sizes
    while offset + SUPERBLOCK_SIZE <= len(data):
        # Check for SquashFS magic number at the current offset
        magic_number = struct.unpack_from("<I", data, offset)[0]  # Read 4 bytes (32-bit) for the magic number

        if magic_number == SQUASHFS_MAGIC:
            print(f"SquashFS partition found at offset: {offset}")

            # Here, we assume the partition continues till the next SquashFS superblock or end of file
            next_partition_offset = find_next_squashfs_partition(data, offset + 512)  # Start next search after the current position
            if next_partition_offset == -1:
                partition_size = len(data) - offset  # If no more partitions, use till end of file
            else:
                partition_size = next_partition_offset - offset  # Partition size is up to the next partition

            # Extract the partition data
            partition_data = data[offset:offset + partition_size]

            # Write the partition to a new file
            output_file = f"{output_prefix}_partition_{partition_count}.img"
            with open(output_file, 'wb') as p:
                p.write(partition_data)
            
            print(f"Partition {partition_count} saved as {output_file}")
            partition_count += 1

            # Continue searching for the next partition without skipping based on partition size
            offset += 512  # Continue searching 512 bytes forward
        else:
            offset += 512  # Move forward by 512 bytes (block size)

def find_next_squashfs_partition(data, start_offset):
    """Helper function to find the next SquashFS partition by searching for the SquashFS magic number."""
    offset = start_offset
    while offset + SUPERBLOCK_SIZE <= len(data):
        magic_number = struct.unpack_from("<I", data, offset)[0]  # Read 4 bytes for the magic number
        if magic_number == SQUASHFS_MAGIC:
            return offset  # Return the start of the next partition
        offset += 512  # Continue searching with block alignment
    return -1  # No further partition found

if __name__ == "__main__":
    input_blob = "flash.bin"  # Path to your binary blob file
    output_prefix = "squashfs_partition"  # Prefix for the output partition files
    extract_squashfs_partitions(input_blob, output_prefix)
