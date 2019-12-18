import sys
import os
import platform
import shutil
import textwrap

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

import json


global jarmuzconfig

if platform.system() == "Windows":
    print("Windows")
    OS_Type = "Windows"
    jarmuz_dir = os.path.abspath(__file__).replace("\\.jarmuz\\jarmuz.py", "")
else:
    OS_Type = "Linux"
    jarmuz_dir = os.path.abspath(__file__).replace("/.jarmuz/jarmuz.py", "")


def write_jarmuzconfig(json_object):
    try:
        os.remove(jarmuz_dir + "/.jarmuz/jarmuzconfig.json")
    except:
        print("Didn't remove a pre-existing file")

    with open(jarmuz_dir + "/.jarmuz/jarmuzconfig.json", "w") as f:
        json.dump(json_object, f, indent=4)


def install_package(package_name):
    split_package_name = package_name.split("/") # Split package name into author and repo name

    print("\nChecking if package is installed...")

    # Check to see if package is already installed
    for i in range(0, len(jarmuzconfig["installed_packages"])):
        if jarmuzconfig["installed_packages"][i]["name"] == package_name:
            print("'{}' is already installed. If you wish to repair it, run 'jarmuz repair packagename'".format(package_name))
            return

    print("Package is not installed, sending request to Jarmuz Garden for package data")

    # Getting url object
    garden_res = 0
    try:
        garden_res = urlopen("http://jarmuz.ngrok.io/fetchprogramdata?programname=" + package_name)
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
    if OS_Type == "Linux":
        if os.path.exists(jarmuz_dir + "/.jarmuz/sources/" + split_package_name[0]):
            os.mkdir(jarmuz_dir + "/.jarmuz/sources/" + split_package_name[0] + "/" + split_package_name[1])
        else:
            os.mkdir(jarmuz_dir + "/.jarmuz/sources/" + split_package_name[0]) 
            os.mkdir(jarmuz_dir + "/.jarmuz/sources/" + split_package_name[0] + "/" + split_package_name[1]) 

        package_dir = jarmuz_dir + "/.jarmuz/sources/" + package_name
    elif OS_Type == "Windows":
        if os.path.exists(jarmuz_dir + "\\.jarmuz\\sources\\" + split_package_name[0]):
            os.mkdir(jarmuz_dir + "\\.jarmuz\\sources\\" + split_package_name[0] + "\\" + split_package_name[1])
        else:
            os.mkdir(jarmuz_dir + "\\.jarmuz\\sources\\" + split_package_name[0]) 
            os.mkdir(jarmuz_dir + "\\.jarmuz\\sources\\" + split_package_name[0] + "\\" + split_package_name[1]) 

        package_dir = jarmuz_dir + "\\.jarmuz\\sources\\" + split_package_name[0] + "\\" + split_package_name[1]


    # Cloning git repo
    print("\nCloning source code from Git Repo")
    os.system("git clone " + package_json_object["sourcerepo"] + " " + package_dir +  " --recursive")

    # Running build commands
    print("\nRunning build commands")
    print(package_dir)
    os.system("cd " + package_dir + "&& " + package_json_object["build_directions"])

    # Adding command to the 'bin' location
    if OS_Type == "Linux":
        with open(jarmuz_dir + "/" + package_json_object["scriptname_unix"], "w") as f:
            for line in zipfile.open(package_json_object["scriptname_unix"]).readlines():
                f.write(line.decode("utf-8").replace("PATH_TO_JARMUZ_PACKAGE", package_dir))
    elif OS_Type == "Windows":
        with open(jarmuz_dir + "\\" + package_json_object["scriptname_unix"], "w") as f:
            for line in zipfile.open(package_json_object["scriptname_unix"]).readlines():
                f.write(line.decode("utf-8").replace("PATH_TO_JARMUZ_PACKAGE", package_dir))



    # Making executable
    if OS_Type == "Linux":
        os.chmod(jarmuz_dir + "/" + package_json_object["scriptname_unix"], 0o777)

    print("\nFinished building {}, use '{}' to run.".format(package_name, package_json_object["scriptname_unix"]))


def remove_package(package_name):
    # Check if package is installed
    target_package = 0
    print()
    for i in range(0, len(jarmuzconfig["installed_packages"])):
        if jarmuzconfig["installed_packages"][i]["name"] == package_name:
            target_package = jarmuzconfig["installed_packages"][i]

    if target_package == 0:
        print("Unable to find package {}. Check your spelling or review .jarmuz/jarmuzconfig.json to check for innaccuracies".format(package_name))
        return

    # Remove bin script
    if OS_Type == "Linux":
        try:
            os.remove(jarmuz_dir + "/" + target_package["scriptname_unix"])
        except:
            print("Unable to remove {}".format(target_package["scriptname_unix"]))
    elif OS_Type == "Windows":
        try:
            os.remove(jarmuz_dir + "\\" + target_package["scriptname_unix"])
        except:
            print("Unable to remove {}".format(target_package["scriptname_unix"]))

    # Remove source directory
    if OS_Type == "Linux":
        try:
            shutil.rmtree(jarmuz_dir + "/.jarmuz/sources/" + target_package["name"].replace("..", ""))
        except:
            print("Unable to remove directory")
    elif OS_Type == "Windows":
        try:
            os.system("rmdir /S /Q " + jarmuz_dir + "\\.jarmuz\\sources\\" + target_package["name"].replace("..", "").replace("/", "\\"))
        except:
            print("Unable to remove directory")


    for i in range(0, len(jarmuzconfig["installed_packages"])):
        if jarmuzconfig["installed_packages"][i]["name"] == package_name:
            print("Deleting {} package".format(target_package["name"]))
            del jarmuzconfig["installed_packages"][i]
            write_jarmuzconfig(jarmuzconfig)
            return

def list_packages():
    package_list = []

    for package in jarmuzconfig["installed_packages"]:
        package_list.append(package["name"])

    sorted_packages = sorted(package_list)

    for package in sorted_packages:
        print(package)


def list_commands():
    filenames = os.listdir(jarmuz_dir)
    filtered_names = []

    for name in filenames:
        if name[0] != ".":
            filtered_names.append(name)
        
    filtered_names = sorted(filtered_names)
    for name in filtered_names:
        print(name)
    
def print_jarmuzinfo():
    print("Jarmuz Application Download Interface")
    print("Cale Overstreet")
    print("December 10th, 2019")

    argument_dict = {
        "commands": "Prints all command names that can be used from the terminal (Be sure the installation directory of Jarmuz is added to your system path)",
        "packages": "Prints the names of every installed package",
        "install packagename": "Installs the specified package, Should be of the form authorname/programname",
        "uninstall packagename": "Uninstalls the specified package. Should be of the form authorname/programname"
    }

    print()
    for key in argument_dict.keys():
        prefix = "{:25s}".format(key)
        preferredwidth = 80
        wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredwidth, subsequent_indent=' '*len(prefix))

        print(wrapper.fill(argument_dict[key]))

def main():
    if os.path.exists(jarmuz_dir + "/.jarmuz/jarmuzconfig.json"):
        with open(jarmuz_dir + "/.jarmuz/jarmuzconfig.json") as f:
            global jarmuzconfig
            jarmuzconfig  = json.load(f)
    else:
        print("jarmuzconfig.json not found, creating one")
        jarmuzconfig = json.loads("{\"installed_packages\": []}")
        write_jarmuzconfig(jarmuzconfig)

    if len(sys.argv) == 1:
        print_jarmuzinfo()

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "install":
            for j in range(i + 1, len(sys.argv)):
                install_package(sys.argv[j])
        elif sys.argv[i] == "uninstall":
            for j in range(i + 1, len(sys.argv)):
                remove_package(sys.argv[j])
        elif sys.argv[i] == "help":
            print_jarmuzinfo()
            return
        elif sys.argv[i] == "commands":
            list_commands()
        elif sys.argv[i] == "packages":
            list_packages()


if __name__ == "__main__":
    main()
