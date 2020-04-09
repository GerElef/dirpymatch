from sys import argv
from os  import listdir
from os.path import isfile, join, dirname, abspath
import subprocess

if len(argv) > 1:
    dir1 = argv[1]
    dir2 = argv[2]
    outdir = argv[3]
    LENGTH = int(argv[4])
    if LENGTH < 2:
        print("Usage: python path/to/dirpymatch.py dir/ect/ory1 dir/ect/ory2 out/put/directory length -exx")
        print("length cannot be under 2")

    if len(argv) == 5:
        EXT_SLICE_FLAG = True if argv[5].upper() == "-EXX" else False
else:
    print("Usage: python path/to/dirpymatch.py dir/ect/ory1 dir/ect/ory2 out/put/directory length -exx\n"
          + "Script takes three directory inputs: first two's contents are compared, and for all files that "
          + "are not duplicate, it copies them into the output directory")
    exit(0)

def getPowershellPath():
    #make recursive function to find powershell.exe automatically later if powershell is not in path
    pass

def getFiles(path):
    actualfiles = []
    for f in listdir(path):
        if isfile(join(path,f)):
            actualfiles.append(f)
    return actualfiles

def sliceStr(s, length):
    substrings = []
    if length <= 2:
        increment = 1
    else:
        increment = -1
    
    while(((len(s) % length) != 0) and length > 2):
        length += 1
    
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
            
def getDirFileNames():
    dir1_names = getFiles(dir1)
    dir2_names = getFiles(dir2)

    dir1_split_names = []
    dir2_split_names = []

    for name in dir1_names:
        dir1_split_names.append(sliceStrExtension(name) if EXT_SLICE_FLAG else sliceStr(name, LENGTH))

    for name in dir2_names:
        dir2_split_names.append(sliceStrExtension(name) if EXT_SLICE_FLAG else sliceStr(name, LENGTH))

    return dir1_names, dir2_names, dir1_split_names, dir2_split_names

def findMatches():
    matches = []
    dir1_match_indexes = []
    dir2_match_indexes = []

    print("Matches found:")
    index  = 0
    for split_name1 in dir1_split_names:
        index2 = 0
        for split_name2 in dir2_split_names:
            if matchStrInList(split_name1, split_name2):
                matches.append(split_name1)
                
                if not (index in dir1_match_indexes):
                    dir1_match_indexes.append(index)
                    
                if not (index2 in dir2_match_indexes):
                    dir2_match_indexes.append(index2)

                print(split_name1)
            
            index2 += 1
        index += 1

    return matches, dir1_match_indexes, dir2_match_indexes

def copyFiles(path, dir_names, match_indexes):
    index = 0
    for name in dir_names:
        if not (index in match_indexes):
            args = ["powershell", "-ExecutionPolicy", "Bypass",
                    f"{dirname(abspath(__file__))}\\copyfiles.ps1", #copyfiles script
                    f"{path}\\{name}",                              #dir + file to copy
                    outdir] 

            instance = subprocess.run(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin  = subprocess.PIPE)
            
        index += 1

if __name__ == "__main__":
    dir1_names, dir2_names, dir1_split_names, dir2_split_names = getDirFileNames()

    matches, dir1_match_indexes, dir2_match_indexes = findMatches()
    
    print()
    print("Starting copy...\n")
    copyFiles(dir1, dir1_names, dir1_match_indexes)
    copyFiles(dir2, dir2_names, dir2_match_indexes)
    print("Copy finished")
