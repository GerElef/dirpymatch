# dirpymatch
Use with command line like this:
python path/to/dirpymatch.py dir/ect/ory1 dir/ect/ory2 out/put/directory length -exx
All contents that are not duplicate in each other will be copied and pasted to the output directory.

Notes for v1.0:
-Performance is poor, even if script is working as intended. May work on it in the future.
-Requires powershell.exe to be in PATH environment variables. Will make this dynamic in the future.
-Add better handling of flags
-Make the program ask you which one of the collisions to copy (1 being first directory, 2 being second, 3 being both, 4 being none)
