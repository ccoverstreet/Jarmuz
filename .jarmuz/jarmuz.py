import sys
import os

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

import json

jarmuz_dir = os.path.abspath(__file__).replace("/.jarmuzsource/jarmuz.py", "")
print(jarmuz_dir)

def installCIS(package_name):
    print("Installing " + package_name)

def main():
    print("Jarmuz")
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "install":
            installCIS(sys.argv[i + 1])

if __name__ == "__main__":
    main()
