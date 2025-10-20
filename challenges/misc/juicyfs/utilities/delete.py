DIR = 'juicefs/mount/are these flags'

import os

files = os.listdir(DIR)
# randomly pick 1/3 files to delete
to_delete = [f for f in files if hash(f) % 10 == 0 and 'ffflllaaaggg' not in f]
print(len(to_delete) / len(files))

for f in to_delete:
    os.remove(os.path.join(DIR, f))