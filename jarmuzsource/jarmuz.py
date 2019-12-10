import sys

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

import json

def installCIS(package_name):
    print("Installing " + package_name)

def main():
    print("Jarmuz")
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "install":
            installCIS(sys.argv[i + 1])

if __name__ == "__main__":
    main()
