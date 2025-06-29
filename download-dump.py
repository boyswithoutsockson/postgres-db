# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "gdown==5.2.0",
# ]
# ///

import gdown

def download_file(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

if __name__ == "__main__":
    file_id = "1fCREZR2suqzdY-lBZzQA3Pm-2acUcXaX"
    destination_path = "data/dump.zip"
    download_file(file_id, destination_path)
    print("done")
