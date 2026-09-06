# Jarmuz: Command Line Utility Management

This is just a quick script for installing and managing command line utilities. Ideally each utility is hosted in a git repostory with a `jarmuz.yaml` file. The file should contain the following

```
build:
    - echo "Some build commands"
    - make
    
artifacts:
    - relative/path/to/output/executables
    - there/can/be/multiple/per/config/file
```

Installed utilities are stored in `~/.local/share/jarmuz` and a config is saved in `~/.config/jarmuz/config.yaml`. 

All artifacts are symlinked to `~/jbin`.

## Installing

```
git clone https://github.com/ccoverstreet/Jarmuz
cd Jarmuz
./jarmuz install .
```

Add `~/jbin` to your path where applicable.

## Using

```
git clone https://gitrepourl.whatever@tag
```
or

```
git clone https://gitrepourl.whatever
```
for cloning main branch

## Updating/Reinstalling

```
jarmuz update
```

When provided with no arguments, `jarmuz update` will attempt to reinstall all packages. This is useful when copying a config to another device/environment and setting up your CLI utilities.
