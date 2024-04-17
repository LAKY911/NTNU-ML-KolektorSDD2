from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import os
import shutil
from tqdm import tqdm 
import urllib.request

# **If URLError -> uncomment the following two lines**
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# 
# **

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path):
    os.makedirs(output_path, exist_ok=True)
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=os.path.join(output_path, "KolektorSDD2.zip"), reporthook=t.update_to)
        with ZipFile(os.path.join(output_path, "KolektorSDD2.zip"), 'r') as zip_ref:
            zip_ref.extractall(output_path)

def move_files(folder):
    # Create subdirectories if they don't exist
    os.makedirs(os.path.join(folder, "masks"), exist_ok=True)
    os.makedirs(os.path.join(folder, "images"), exist_ok=True)
    for filename in tqdm([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]):
        if "_GT" in filename:
            shutil.move(os.path.join(folder, filename), os.path.join(folder, "masks", filename))
        else:
            shutil.move(os.path.join(folder, filename), os.path.join(folder, "images", filename))

if __name__ == "__main__":

    ZIP_URL = 'http://go.vicos.si/kolektorsdd2'
    DATA_PATH = './datasets/KolektorSDD3/'

    # Download and extract dataset
    download_url(ZIP_URL, DATA_PATH)    
    print('Done downloading and extracting KolektorSDD2 dataset.')

    # Move files to respective subfolders
    move_files(os.path.join(DATA_PATH, 'train/'))
    move_files(os.path.join(DATA_PATH, 'test/'))

    print("Done sorting images.")