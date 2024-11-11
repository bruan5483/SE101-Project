from dotenv import load_dotenv, dotenv_values
import os

# load dotenv
load_dotenv()

merge_file_path = os.getenv("MERGE_FILE_PATH")


def parse_mergefile(toedit,mergefile):
    readingcode = open(toedit,"r")
    cached_codefile=readingcode.readlines()
    readingcode.close()

    print (cached_codefile)

    updated_codefile=cached_codefile

    with open(mergefile) as tomerge:
        for line in tomerge:
            print(line)
            parsedline=parse_line(line.rstrip())
            print(parsedline)
            updated_codefile=update_contents(parsedline,updated_codefile)
    
    print (updated_codefile)
    update_codefile(updated_codefile,toedit)

def parse_line(l)->(int, int, str):
    splitstring=l.split(',')
    #add error detection
    linenum=int(splitstring[0])
    index=int(splitstring[1])

    stuff=splitstring[2]
    for i in range(3,len(splitstring)):
        stuff+=","+splitstring[i]

    stuff=stuff.replace("[newline]", "\n")

    stuff=stuff.replace("[comment]", " //") #relace with function to get correct comment characters

    #add other parsing features

    return (linenum,index,stuff)

def update_contents(tochange:tuple[int,int,str],contents):
    if (tochange[1]==-1):
        contents[tochange[0]]=contents[tochange[0]].rstrip()
        contents[tochange[0]]+=tochange[2]

    elif (tochange[1]==0):
        contents.insert(tochange[0]-1,tochange[2])
    
    #else:
        #handle inserting to the middle of a line
    
    return contents

def update_codefile(contents,writepath):
    with open(writepath,"w") as writefile:
        writefile.writelines(contents)

file_to_edit="./codestuff.c"


parse_mergefile(file_to_edit, merge_file_path)
