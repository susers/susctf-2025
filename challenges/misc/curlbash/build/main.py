import subprocess
import os
import hashlib
import requests


ROOT = "/app"
TEST_SCRIPT_PATH = "testscript.sh"

CURLBASH = """
#!/bin/bash

curl -fsSL {url} | bash -re
"""


def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def snapshot_directory(*paths):
    file_hashes = {}
    for path in paths:
        for root, dirs, files in os.walk(path):
            for f in files:
                full_path = os.path.join(root, f)
                try:
                    file_hashes[full_path] = hash_file(full_path)
                except Exception:
                    pass
    return file_hashes


def fetch(url):
    result = requests.get(url)
    result.raise_for_status()
    return result.text


def fetch_with_curl(url):
    result = subprocess.run(["curl", "-fsSL", url], capture_output=True, text=True)
    if result.returncode != 0:
        print("Failed to download script!")
        exit(1)
    return result.stdout


def write_script_to_chroot(script_path, script_content):
    content = "readonly LD_PRELOAD\n" + script_content
    script_file = os.path.join(ROOT, script_path)
    with open(script_file, "w") as f:
        f.write(content)
    os.chmod(script_file, 0o755)


def run_bash_script(script_path, sandbox=True):
    script_path = os.path.join(ROOT, script_path)
    sandbox_cmd = ["/bin/bash", "-re", script_path]
    if sandbox:
        # qemu-x86_64 is a safe sandbox with isolated network & filesystem
        # try locally with "unshare -n"
        sandbox_cmd.insert(0, "qemu-x86_64")
    result = subprocess.run(sandbox_cmd, capture_output=True, text=True)
    # print("Script stdout:", result.stdout)
    # print("Script stderr:", result.stderr)
    print("Exit code:", result.returncode)
    if result.returncode != 0:
        print("Ah-oh exit code. You fail!")
        exit(1)


def run_sandboxed(url):
    # fetch first
    s = fetch_with_curl(url)
    if s != fetch(url):
        print("WTH did you give me?")
        exit(1)
    write_script_to_chroot(TEST_SCRIPT_PATH, s)
    # Snapshot root filesystem before running script
    root_snapshot_before = snapshot_directory(ROOT, "/tmp", "/dev/shm")

    # Run script sandboxed
    run_bash_script(TEST_SCRIPT_PATH)

    # Snapshot root filesystem after running script
    root_snapshot_after = snapshot_directory(ROOT, "/tmp", "/dev/shm")

    # Compare snapshots for any changes
    changed_files = []
    for fpath, hsh in root_snapshot_before.items():
        if fpath in root_snapshot_after:
            if root_snapshot_after[fpath] != hsh:
                changed_files.append(fpath)
        else:
            changed_files.append(fpath + " (deleted)")

    new_files = [f for f in root_snapshot_after if f not in root_snapshot_before]

    if not changed_files and not new_files:
        print("No disk files were modified by the script. Good!")
    else:
        print(f"Files changed: {changed_files}")
        print(f"New files: {new_files}")
        print("Some disk files were modified. You fail.")
        exit(1)


def run_curlbash(url):
    write_script_to_chroot(TEST_SCRIPT_PATH, CURLBASH.format(url=url))
    run_bash_script(TEST_SCRIPT_PATH, sandbox=False)


def main():
    url = input("Your script: ")

    # Run random times in sandbox (to make sure you are not spoofing)
    random_index = int.from_bytes(os.urandom(1), "big") % 32
    for i in range(random_index):
        print(f"[Round {i}]", end=" ")
        run_sandboxed(url)

    # Since the content is safe, do it in curlbash this time
    print(f"[Round {random_index} CURLBASH]", end=" ")
    run_curlbash(url)


if __name__ == "__main__":
    main()
