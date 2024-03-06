from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

# **If URLError -> uncomment the following two lines**
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# 
# **

if __name__ == "__main__":

    zipurl = 'http://go.vicos.si/kolektorsdd2'

    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall('./datasets/KolektorSDD2/')
    
    print('Done downloading and extracting KolektorSDD2 dataset.')