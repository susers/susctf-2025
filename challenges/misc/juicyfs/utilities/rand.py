import os
import random
import string
import time

def generate_random_name(length=12):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_random_file(directory):
    filename = generate_random_name()
    filepath = os.path.join(directory, filename)

    # Determine a random size between 10 KB and 2 MB.
    # 10 KB = 10 * 1024 bytes
    # 2 MB = 2 * 1024 * 1024 bytes
    # min_size = 1 * 1024 * 1024
    min_size = 1024
    # max_size = 5 * 1024 * 1024
    max_size = 100 * 1024
    size = random.randint(min_size, max_size)

    content = os.urandom(size)

    try:
        with open(filepath, 'wb') as f:
            f.write(content)
        # Convert size to KB for friendlier output
        size_kb = size / 1024
        print(f"Successfully created: {filepath} ({size_kb:.2f} KB)")
    except IOError as e:
        print(f"Error creating file {filepath}: {e}")


def main():
    """
    Main function to run the script.
    """
    output_dir = "juicefs/mount/are these flags"

    while True:
        create_random_file(output_dir)
        time.sleep(0.1)
        # time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    main()
