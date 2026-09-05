# Design goals

I want a system where I can quickly install utilities I normally use on a system in a reproducible manner

- Ideas
    - Makefiles with specific fields (ex. jinstall, jremove)
    - YAML file with specific fields
        - Fields
            - build
                - Commands needed to build output
            - artifacts
                - Array of strings containing the relative path (within project) of executable artifacts that need to be symlinked to the shared bin
        - Jarmuz utility would keep a `.config/jarmuz/config.yaml` file with a list of installed packages
        - Jarmuz utility would download/store packages in `~/.local/share/jarmuz`
            - For GitHub hosted packages, they would be downloaded into `~/.local/share/jarmuz`
            - Local directories would not be copied into share

