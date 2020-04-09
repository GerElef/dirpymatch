from sys import argv
from os  import listdir
from os.path import isfile, join

if len(argv) > 1:
    dir1 = argv[1]
    dir2 = argv[2]
    LENGTH = int(argv[3])
    EXT_SLICE_FLAG = True if argv[4].upper() == "-EXX" else False
else:
    print("Usage: python.exe path/to/dirpymatch.py dir/ect/ory1 dir/ect/ory2 length -exx")
    exit(0)

def getFiles(path):
    actualfiles = []
    for f in listdir(path):
        if isfile(join(path,f)):
            actualfiles.append(f)
    return actualfiles

def sliceStr(s, length):
    substrings = []
    for i in range(0, len(s), length):
        if '.' in s[i : i+length]:
            substrings.append(s[s.find('.')+1 : len(s)])
            break
        
        substrings.append(s[i : i+length])
    return substrings

def sliceStrExtension(s):
    return s.split('.')

def matchStrInList(l1, l2):
    if l1[-1] == l2[-1]:
        #doesn't include the extension as a substring
        substrings = l1[0:len(l1) -1]
        for substring in substrings:
            for string in l2[0:len(l2)-1]:
                if string.find(substring) != -1:
                    return True
    return False
            

dir1_names = getFiles(dir1)
dir2_names = getFiles(dir2)

dir1_split_names = []
dir2_split_names = []

for name in dir1_names:
    dir1_split_names.append(sliceStrExtension(name) if EXT_SLICE_FLAG else sliceStr(name, LENGTH))

for name in dir2_names:
    dir2_split_names.append(sliceStrExtension(name) if EXT_SLICE_FLAG else sliceStr(name, LENGTH))

matches = []

for split_name1 in dir1_split_names:
    for split_name2 in dir2_split_names:
        if matchStrInList(split_name1, split_name2):
            matches.append(f"Match Found{split_name1} {split_name2}")

for match in matches:
    print(match)
