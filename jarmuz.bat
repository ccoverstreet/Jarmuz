SET rootdir=%~dp0
echo %rootdir:~0,-1%

python %rootdir%/.jarmuz/jarmuz.py %*
