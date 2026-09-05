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
