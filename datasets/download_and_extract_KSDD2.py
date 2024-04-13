from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import os
import shutil
from tqdm import tqdm 

# **If URLError -> uncomment the following two lines**
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# 
# **


import time


if __name__ == "__main__":

    zipurl = 'http://go.vicos.si/kolektorsdd2'

    with urlopen(zipurl) as zipresp:
        print("Downloading")
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall('./datasets/KolektorSDD2/')
    
    print('Done downloading and extracting KolektorSDD2 dataset.')

    DATA_TRAIN = "./datasets/KolektorSDD2/train/"
    DATA_TEST = "./datasets/KolektorSDD2/test/"


    def move_files(folder):
        # Create subdirectories if they don't exist
        os.makedirs(os.path.join(folder, "masks"), exist_ok=True)
        os.makedirs(os.path.join(folder, "images"), exist_ok=True)
        for filename in tqdm([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]):
            if "_GT" in filename:
                shutil.move(os.path.join(folder, filename), os.path.join(folder, "masks", filename))
            else:
                shutil.move(os.path.join(folder, filename), os.path.join(folder, "images", filename))

    # Move files to respective subfolders
    move_files(DATA_TRAIN)
    move_files(DATA_TEST)

    print("Done sorting images.")