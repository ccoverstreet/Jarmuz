import sys
import os

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

import json

global jarmuzconfig


jarmuz_dir = os.path.abspath(__file__).replace("/.jarmuz/jarmuz.py", "")


def write_jarmuzconfig(json_object):
    os.remove(jarmuz_dir + "/.jarmuz/jarmuzconfig.json")
    with open(jarmuz_dir + "/.jarmuz/jarmuzconfig.json", "w") as f:
        json.dump(json_object, f, indent=4) 
        

def install_package(package_name):
    split_package_name = package_name.split("/") # Split package name into author and repo name

    print("Checking if package is installed...")
    
    # Check to see if package is already installed
    for i in range(0, len(jarmuzconfig["installed_packages"])):
        if jarmuzconfig["installed_packages"][i]["name"] == package_name:
            print("'{}' is already installed. If you wish to repair it, run 'jarmuz repair packagename'".format(package_name))
            return
            
    print("Package is not installed, sending request to Jarmuz Garden for package data")

    # Getting url object
    garden_res = 0
    try:
        garden_res = urlopen("http://localhost:9420/fetchprogramdata?programname=" + package_name)
    except:
        print("Package not found in Jarmuz Garden")
        return

    # Reading to zipfile object
    zipfile = ZipFile(BytesIO(garden_res.read()))

    # Getting json string to load into json object
    package_json_string = ""
    for line in zipfile.open(split_package_name[0] + "_" + split_package_name[1] + ".json").readlines():
        package_json_string += line.decode("utf-8")

    # Loading json string into object
    package_json_object = json.loads(package_json_string)
    
    # Adding new package data to json
    jarmuzconfig["installed_packages"].append(package_json_object)
    write_jarmuzconfig(jarmuzconfig) # Writing new json to config file

    # Creating directory for source code
    if os.path.exists(jarmuz_dir + "/.jarmuz/sources/" + split_package_name[0]):
        os.mkdir(jarmuz_dir + "/.jarmuz/sources/" + split_package_name[0] + "/" + split_package_name[1])
    else:
        os.mkdir(jarmuz_dir + "/.jarmuz/sources/" + split_package_name[0]) 
        os.mkdir(jarmuz_dir + "/.jarmuz/sources/" + split_package_name[0] + "/" + split_package_name[1]) 

    package_dir = jarmuz_dir + "/.jarmuz/sources/" + package_name


    # Cloning git repo
    print("\nCloning source code from Git Repo")
    os.system("git clone " + package_json_object["sourcerepo"] + " " + package_dir +  " --recursive")

    # Running build commands
    print("\nRunning build commands")
    os.system("cd " + package_dir + ";" + package_json_object["build_directions"])

    # Adding command to the 'bin' location
    with open(jarmuz_dir + "/" + package_json_object["scriptname_unix"], "w") as f:
        for line in zipfile.open(package_json_object["scriptname_unix"]).readlines():
            f.write(line.decode("utf-8").replace("PATH_TO_JARMUZ_PACKAGE", package_dir))

    # Making executable
    os.chmod(jarmuz_dir + "/" + package_json_object["scriptname_unix"], 0o777)

    print("\nFinished building {}, use '{}' to run.".format(package_name, package_json_object["scriptname_unix"]))


def remove_package(package_name):
    # Check if package is installed
    target_package = 0
    for i in range(0, len(jarmuzconfig["installed_packages"])):
        if jarmuzconfig["installed_packages"][i]["name"] == package_name:
            print("Deleting {} package")
            target_package = jarmuzconfig["installed_packages"][i]
            return

    # Remove bin script
    try:
        os.remove(jarmuz_dir + "/" + target_package["scriptname_unix"])
    except:
        print("Unable to remove {}".format(target_package["scriptname_unix"]))

    # Remove source directory
    try:
        os.rmtree(jarmuz_dir + "/.jarmuz/sources/" + target_package["name"])


    

def main():
    with open(jarmuz_dir + "/.jarmuz/jarmuzconfig.json") as f:
        global jarmuzconfig
        jarmuzconfig  = json.load(f)


    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "install":
            install_package(sys.argv[i + 1])

if __name__ == "__main__":
    main()
