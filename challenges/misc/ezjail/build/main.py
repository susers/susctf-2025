import subprocess
import os
import hashlib
import requests


ROOT = "/app"
TEST_SCRIPT_PATH = "testscript.sh"


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
    r = requests.get(url)
    r.raise_for_status()
    return r.text


def write_script_to_chroot(script_path, script_content):
    content = "readonly LD_PRELOAD\n" + script_content
    script_file = os.path.join(ROOT, script_path)
    with open(script_file, "w") as f:
        f.write(content)
    os.chmod(script_file, 0o755)


def run_bash_script_sandbox(script_path):
    script_path = os.path.join(ROOT, script_path)
    env = {"LD_PRELOAD": "./override.so"}
    sandbox_cmd = ["bash", "-re", script_path]
    result = subprocess.run(sandbox_cmd, capture_output=True, text=True, env=env)
    return result


def main():
    url = input("Your script: ")
    s = fetch(url)
    write_script_to_chroot(TEST_SCRIPT_PATH, s)

    # Snapshot root filesystem before running script
    root_snapshot_before = snapshot_directory(ROOT, "/tmp", "/dev/shm")

    # Run script sandboxed
    result = run_bash_script_sandbox(TEST_SCRIPT_PATH)
    print("Script stdout:", result.stdout)
    print("Script stderr:", result.stderr)
    print("Exit code:", result.returncode)
    if result.returncode != 0:
        print("Ah-oh exit code. You fail!")
        exit(1)

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


if __name__ == "__main__":
    main()
