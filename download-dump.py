# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "gdown==5.2.0",
# ]
# ///

import gdown
import zipfile
import os

def download_file(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

def unzip_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as z:
        z.extractall(os.path.dirname(file_path))

if __name__ == "__main__":
    file_id = "1cQb23nkz-DAlo33cU96BnPjdnXU9MoFA"
    destination_path = "data/dump.zip"
    os.makedirs("data", exist_ok=True)
    download_file(file_id, destination_path)
    unzip_file(destination_path)
    os.remove(destination_path)
    print(f"done with {destination_path.split('/')[-1]}")

    file_id = "1K0ykFwVEdU-EmwSPC_p6Yx-S4Ko5Bylh"
    destination_path = "frontend/src/assets/photos-2023-2026.zip"
    download_file(file_id, destination_path)
    unzip_file(destination_path)
    os.remove(destination_path)
    print(f"done with {destination_path.split('/')[-1]}")
