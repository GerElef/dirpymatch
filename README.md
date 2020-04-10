# dirpymatch
Use with command line like this:
python path/to/dirpymatch.py dir/ect/ory1 dir/ect/ory2 out/put/directory length -exx stringfilter
All contents that are not duplicate in each other will be copied and pasted to the output directory.

Notes for v1.0:

-Performance is poor due to opening up a new subprocess for each copy. Will work on it in the future.

-Requires powershell.exe to be in PATH environment variables. Will make this dynamic in the future.

-Add better handling of flags


To-Do:

-Add a double-pass check on the output folder for possible duplicates

-Convert substring logic to automatically generated regex (?)
