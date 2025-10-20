import os
import random
import sys
import hashlib
import time

# --- Configuration ---
# The base size for logically dividing the file.
BASE_CHUNK_SIZE = 409600 * 3
# The percentage of logical chunks to write in the first pass (0.0 to 1.0)
FIRST_PASS_PERCENTAGE = 1.0
# --- End Configuration ---

def get_random_chunk_size(min_size, max_size):
    """Returns a random chunk size within the given range."""
    # return random.randint(min_size, max_size)
    return BASE_CHUNK_SIZE

def calculate_file_hash(file_path):
    """Calculates and returns the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError as e:
        print(f"Error reading file for hashing: {e}")
        return None

def _write_pass(pass_name, indices, num_chunks, source_path, dest_path, file_size, min_chunk_size, max_chunk_size):
    """Helper function to perform a pass of writing logical chunks."""
    print(f"\n[Phase {3 if pass_name == 'Pass 1' else 4}] Starting {pass_name.lower()}, writing {len(indices)} randomly selected logical chunks...")
    for i, index in enumerate(indices):
        offset = index * BASE_CHUNK_SIZE
        bytes_to_process = min(BASE_CHUNK_SIZE, file_size - offset)

        # Read the entire logical block from the source file
        with open(source_path, 'rb') as f_src:
            f_src.seek(offset)
            data_block = f_src.read(bytes_to_process)

        # Write the block in smaller, random sub-chunks, closing the file each time
        bytes_written_for_block = 0
        while bytes_written_for_block < len(data_block):
            sub_chunk_size = get_random_chunk_size(min_chunk_size, max_chunk_size)
            sub_chunk_data = data_block[bytes_written_for_block : bytes_written_for_block + sub_chunk_size]

            # Open, seek, write, close for each sub-chunk
            with open(dest_path, 'rb+') as f_dest:
                f_dest.seek(offset + bytes_written_for_block)
                f_dest.write(sub_chunk_data)
            
            time.sleep(5)

            bytes_written_for_block += len(sub_chunk_data)

        print(f"  -> Wrote logical chunk {index+1}/{num_chunks} ({pass_name}: {i+1}/{len(indices)})")

    print(f"✅ {pass_name} complete.")
    time.sleep(1)

def unnecessary_copy(source_path, dest_path):
    """
    Copies a file from source to destination by first writing random data,
    then overwriting it in two separate, randomized passes with the real data.
    Each write operation uses a random chunk size and closes the file.
    """
    try:
        # --- Step 1: Get source file size ---
        if not os.path.exists(source_path):
            print(f"❌ Error: Source file not found at '{source_path}'")
            return

        file_size = os.path.getsize(source_path)
        print(f"Source: '{source_path}' ({file_size} bytes)")
        print(f"Destination: '{dest_path}'")

        # --- Dynamically set chunk size based on file size ---
        if file_size < 1 * 1024 * 1024:  # < 1 MB
            min_chunk_size, max_chunk_size = 512, 4096
        elif file_size < 50 * 1024 * 1024: # < 50 MB
            min_chunk_size, max_chunk_size = 10240, 81920
        elif file_size < 200 * 1024 * 1024: # < 200 MB
            min_chunk_size, max_chunk_size = 40960, 327680
        else: # >= 200 MB
            min_chunk_size, max_chunk_size = 81920, 655360
        print(f"Dynamic chunk size range set to: {min_chunk_size}-{max_chunk_size} bytes")


        # --- Step 2: Create a file of the same size filled with null bytes ---
        # print("\n[Phase 1] Creating destination file filled with null bytes...")
        # try:
        #     with open(dest_path, 'wb') as f_dest:
        #         if file_size > 0:
        #             f_dest.seek(file_size - 1)
        #             f_dest.write(b'\0')
        #     print("✅ Null file created successfully.")
        # except IOError as e:
        #     # Handle cases where seek might fail for very large files on some systems
        #     print(f"  -> Seek method failed ({e}), falling back to iterative write...")
        #     with open(dest_path, 'wb') as f_dest:
        #         null_chunk = os.urandom(1024 * 1024)
        #         bytes_written = 0
        #         while bytes_written < file_size:
        #             bytes_to_write = min(len(null_chunk), file_size - bytes_written)
        #             f_dest.write(null_chunk[:bytes_to_write])
        #             bytes_written += bytes_to_write
        #     print("✅ Null file created successfully with fallback method.")

        # time.sleep(5) # Pause for dramatic effect

        # --- Step 3: Determine and shuffle the logical chunks ---
        num_chunks = (file_size + BASE_CHUNK_SIZE - 1) // BASE_CHUNK_SIZE
        chunk_indices = list(range(num_chunks))
        random.shuffle(chunk_indices)
        print(f"\n[Phase 2] File divided into {num_chunks} logical chunks. Order randomized.")

        # Split indices for the two passes
        split_point = int(num_chunks * FIRST_PASS_PERCENTAGE)
        first_pass_indices = chunk_indices[:split_point]
        second_pass_indices = chunk_indices[split_point:]

        # --- Step 4 & 5: Write the real data in two passes ---
        _write_pass("Pass 1", first_pass_indices, num_chunks, source_path, dest_path, file_size, min_chunk_size, max_chunk_size)
        _write_pass("Pass 2", second_pass_indices, num_chunks, source_path, dest_path, file_size, min_chunk_size, max_chunk_size)

        # --- Step 6: Verification ---
        print("\n[Phase 5] Verifying copy...")
        source_hash = calculate_file_hash(source_path)
        dest_hash = calculate_file_hash(dest_path)

        print(f"  Source SHA256:      {source_hash}")
        print(f"  Destination SHA256: {dest_hash}")

        if source_hash and dest_hash and source_hash == dest_hash:
            print("\n🎉 Success! Files are identical. The unnecessary copy is complete.")
        else:
            print("\n🔥 Failure! File hashes do not match. Something went wrong.")

    except IOError as e:
        print(f"❌ An I/O error occurred: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) != 3:
        print("A fantastically inefficient file copier.")
        print("\nUsage: python unnecessary_copy.py <source_file> <destination_file>")
        sys.exit(1)

    source = sys.argv[1]
    destination = sys.argv[2]
    unnecessary_copy(source, destination)

if __name__ == "__main__":
    main()

