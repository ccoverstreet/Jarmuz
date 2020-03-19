# Jarmuz
Command-line program for installing and running programs from Git Repositories

___
## About
Jarmuz is meant as an easy way to download and run programs from Github repositories. The goal of Jarmuz was to make it easy to make programs I've written easier to access when working on a different computer. By just adding the root of Jarmuz to your system's PATH, running a command like `jarmuz install ccoverstreet/CIS` and then `jarmuz start ccoverstreet/CIS`. In order for a repository to be downloadable from Jarmuz, the repository must contain a jarmuzpackage.json containing the following information:

#### !IMPORTANT, this jarmuzpackage.json file setup will be modified in Version 1.1 to accomodate differences between platforms like python vs python3 or differences in filepath formats (looking at you Windows).
```
{
  "build": "make", // Commands necessary to build Github repository program. Simple case is just using a makefile.
  "start": "./programexecutable", // Commands needed to start, could also be something like python myfile.py
}
```
