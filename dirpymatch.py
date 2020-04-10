from sys import argv
from os  import listdir
from os.path import isfile, join, dirname, abspath
import subprocess

if len(argv) >= 6:
    dir1 = argv[1]
    dir2 = argv[2]
    outdir = argv[3]
    LENGTH = int(argv[4])
    if LENGTH < 2:
        print("Usage: python path/to/dirpymatch.py dir/ect/ory1 dir/ect/ory2 out/put/directory length -exx")
        print("Length cannot be under 2")

    EXT_SLICE_FLAG = True if argv[5].upper() == "-EXX" else False
    IGNORE_FLAG = False

    if len(argv) == 7:
        IGNORE_FLAG = True
        IGNORE_PARAMETER = argv[6]
        
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

    i = 0
    dotcount = 0
    dotpos = []
    for c in s:
        if c == '.':
            dotcount += 1
            dotpos.append(i)
        i += 1
    
    while(((dotpos[-1] % length) != 0) and length > 2):
        length += increment
    
    for i in range(0, dotpos[-1], length):
        substrings.append(s[i : i+length])
    
    substrings.append(s[dotpos[-1] + 1:len(s)])
        
    return substrings


def sliceStrExtension(s):
    i = 0
    dotcount = 0
    dotpos = []
    for c in s:
        if c == '.':
            dotcount += 1
            dotpos.append(i)
        i += 1
    return [s[0:dotpos[-1]], s[dotpos[-1] + 1:len(s)]]


def matchStrInList(l1, l2):
    if l1[-1] == l2[-1]:
        #doesn't include the extension as a substring
        substrings = l1[0:len(l1) -1]
        for substring in substrings:
            for string in l2[0:len(l2)-1]:
                if string.find(substring) != -1:
                    if IGNORE_FLAG:
                        if substring == IGNORE_PARAMETER:
                            continue
                    
                    return True
    return False

            
def getDirFileNames():
    global EXT_SLICE_FLAG
    
    dir1_names = getFiles(dir1)
    dir2_names = getFiles(dir2)

    dir1_split_names = []
    dir2_split_names = []

    for name in dir1_names:
        dir1_split_names.append(sliceStrExtension(name) if EXT_SLICE_FLAG else sliceStr(name, LENGTH))

    for name in dir2_names:
        dir2_split_names.append(sliceStrExtension(name) if EXT_SLICE_FLAG else sliceStr(name, LENGTH))

    return dir1_names, dir2_names, dir1_split_names, dir2_split_names


def handleCollision(name1, name2, index1, index2, prev_collisions):
    user_input = ""
    VALID_INPUTS = ["1", "2", "3", "4"]
    path1flag = False
    path2flag = False
    for collision in prev_collisions:
        if name1[index1] in collision:
            path1flag = True
        if name2[index2] in collision:
            path2flag = True
    
    if path1flag and path2flag: #if both files exist, add none
        print(f"Collision between: {name1[index1]} and {name2[index2]}. Solving by not adding anything...")
        return 4
    elif path1flag: #if first file exists, add the second one
        print(f"Collision between: {name1[index1]} and {name2[index2]}. Solving by adding {name2[index2]}...")
        return 2
    elif path2flag: #if second file exists, add the second one
        print(f"Collision between: {name1[index1]} and {name2[index2]}. Solving by adding {name1[index1]}...")
        return 1

    #if none of the two files exist, let the user pick
    while(user_input not in VALID_INPUTS):
        user_input = input(f"Collision between: {name1[index1]} and {name2[index2]}\n"
                           +f"Enter 1 to copy {name1[index1]}.\nEnter 2 to copy {name2[index2]}.\n"
                           + "Enter 3 to copy both.\nEnter 4 to do nothing.")

    #1 equivalent to adding only the 1st file
    #2 equivalent to adding only the 2nd file
    #3 equivalent to returning false. do not resume (add all)
    #4 equivalent to returning true. resume as normal (do not add)
    return int(user_input)

def findMatches():
    matches = []
    dir1_toAdd = []
    dir2_toAdd = []
    prev_collisions = []

    print("Collisions found:")
    index  = 0
    for split_name1 in dir1_split_names:
        index2 = 0
        for split_name2 in dir2_split_names:
            if matchStrInList(split_name1, split_name2):
                user_input = handleCollision(dir1_names, dir2_names, index, index2, prev_collisions)
                if user_input == 4:
                    matches.append(split_name1)
                    
                elif user_input == 3:
                    prev_collisions.append(f"{dir2_names[index2]}")
                    prev_collisions.append(f"{dir1_names[index]}")
                    
                    dir2_toAdd.append(f"{dir2_names[index2]}")
                    dir1_toAdd.append(f"{dir1_names[index]}")
                    
                elif user_input == 2:
                    prev_collisions.append(f"{dir2_names[index2]}")
                    dir2_toAdd.append(f"{dir2_names[index2]}")
                    
                elif user_input == 1:
                    prev_collisions.append(f"{dir1_names[index]}")
                    dir1_toAdd.append(f"{dir1_names[index]}")
                    
            else:
                if (not dir1_names[index] in dir1_toAdd) and (not dir1_names[index] in prev_collisions):
                    print(f"Noncollision: Added {dir1_names[index]}")
                    prev_collisions.append(f"{dir1_names[index]}")
                    dir1_toAdd.append(f"{dir1_names[index]}")

                if (not dir2_names[index2] in dir2_toAdd) and (not dir2_names[index2] in prev_collisions):
                    print(f"Noncollision: Added {dir2_names[index2]}")
                    prev_collisions.append(f"{dir2_names[index2]}")
                    dir2_toAdd.append(f"{dir2_names[index2]}")
                
            index2 += 1

        index += 1

    return matches, dir1_toAdd, dir2_toAdd


def copyFiles(path, dir_names):#, match_indexes):
    for name in dir_names:
        print(f"Copying {path}\\{name} ...")
        args = ["powershell", "-ExecutionPolicy", "Bypass", "-file",
                f'{dirname(abspath(__file__))}\\copyfiles.ps1', #copyfiles script
                f'{path}\\{name}',                              #dir + file to copy
                outdir]
        instance = subprocess.run(args, shell=True)

if __name__ == "__main__":
    dir1_names, dir2_names, dir1_split_names, dir2_split_names = getDirFileNames()

    matches, dir1_toAdd, dir2_toAdd = findMatches()
    
    print()
    print("Starting copy...\n")
    copyFiles(dir1, dir1_toAdd)
    copyFiles(dir2, dir2_toAdd)#
    print("Copy finished")
