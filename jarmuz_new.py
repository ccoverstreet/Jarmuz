# Jarmuz: Jarmuz.py
# Cale Overstreet
# March 18, 2020
# This is the primary Jarmuz script that is used for managed programs installed from Github. This script should be kept compatible on all platforms supported by Python.


import sys
import os
import shutil

import json

# Home directory of Jarmuz
jarmuz_dir = os.path.abspath(__file__).replace("/jarmuz_new.py", "")

cwd = os.getcwd()

def jarmuz_install(arguments):
    for i in range(0, len(arguments)):
        if len(arguments[i].split("/")) != 2:
            print("The argument \"{}\"".format(arguments[i]))
            print(" -> Should be formatted like \"author/gitname\"")
            return

        try:
            res = os.system("git clone --recursive https://github.com/{} {}".format(arguments[i], jarmuz_dir + "/sources/" + arguments[i]))
            if res != 0:
                print("FATAL: Error when calling Git. Check any above errors")
                return

        except:
            print("FATAL: Unable to retrieve package {}. Check input for typos".format(arguments[i]))
            return

        try: 
            with open(jarmuz_dir + "/sources/" + arguments[i] + "/jarmuzpackage.json") as f:
                data = json.load(f)
             

            os.chdir(jarmuz_dir + "/sources/" + arguments[i])
            os.system(data["build"])
            os.chdir(cwd)

        except:
            print("FATAL: Unable to find Jarmuz Package file")



def jarmuz_remove(arguments):
    for i in range(0, len(arguments)):
        if len(arguments[i].split("/")) != 2:
            print("The argument \"{}\"".format(arguments[i]))
            print(" -> Should be formatted like \"author/gitname\"")
            return

        try:
            shutil.rmtree(jarmuz_dir + "/sources/" + arguments[i])
        except:
            print("FATAL: Unable to remove requested package")


def jarmuz_start(arguments):
    for i in range(0, len(arguments)):
        if len(arguments[i].split("/")) != 2:
            print("The argument \"{}\"".format(arguments[i]))
            print(" -> Should be formatted like \"author/gitname\"")
            return

        try: 
            with open(jarmuz_dir + "/sources/" + arguments[i] + "/jarmuzpackage.json") as f:
                data = json.load(f)
             

            os.chdir(jarmuz_dir + "/sources/" + arguments[i])
            os.system(data["start"])
            os.chdir(cwd)

        except:
            print("FATAL: Unable to start package")




def main():
    # Main execution sequence tht determines what helper functions are needed

    # Loop through all arguments
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "install":
            jarmuz_install(sys.argv[i + 1:len(sys.argv)]) # Sends remaining argumens to helper function
        elif sys.argv[i] == "remove":
            jarmuz_remove(sys.argv[i + 1: len(sys.argv)])
        elif sys.argv[i] == "start":
            jarmuz_start(sys.argv[i + 1: len(sys.argv)])


if __name__ == "__main__":
    main()
