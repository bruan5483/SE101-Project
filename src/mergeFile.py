from dotenv import load_dotenv
import os
import OCRText
import generateMergeFile
import imageProcessing

# load dotenv
load_dotenv()

MERGE_FILE_PATH = os.getenv("MERGE_FILE_PATH")


def parse_mergefile(toedit, mergefile):
    readingcode = open(toedit,"r")
    cached_codefile=readingcode.readlines()
    readingcode.close()

    # print (cached_codefile)

    updated_codefile=cached_codefile

    with open(mergefile) as tomerge:
        for line in tomerge:
            # print(line)
            parsedline=parse_line(line.rstrip(), toedit)
            # print(parsedline)
            updated_codefile=update_contents(parsedline,updated_codefile)
    
    # print (updated_codefile)
    update_codefile(updated_codefile,toedit)

def parse_line(l, toedit)->(int, int, str):
    # print(l)
    splitstring=l.split(',')
    #add error detection
    linenum=int(splitstring[0]) - 1 # start from 1 index for line num
    index=int(splitstring[1])

    stuff=splitstring[2]
    for i in range(3,len(splitstring)):
        stuff+=","+splitstring[i]

    stuff=stuff.replace("[newline]", "\n")

    comment_char = getCommentChar(toedit)
    stuff=stuff.replace("[comment]", comment_char) #relace with function to get correct comment characters

    #add other parsing features

    return (linenum,index,stuff)

def getCommentChar(code_file):
    commentChar = {"py": " #", 
                   "c": " //",
                   "cpp": " //",
                   "cc": " //",
                   "java": " //",
                   "js": " //",
                   "sql": " --",
                   "rb": " //",
                   "r": " #"}
    
    language = code_file.split(".")[-1]
    if language in commentChar:
        return commentChar[language]
    # default comment type 
    return " //"


def update_contents(tochange:tuple[int,int,str],contents):
    if (tochange[1]==-1):
        contents[tochange[0]]=contents[tochange[0]].rstrip()
        contents[tochange[0]]+=tochange[2]

    elif (tochange[1]==0):
        contents.insert(tochange[0],tochange[2])
    
    #else:
        #handle inserting to the middle of a line
    
    return contents

def update_codefile(contents,writepath):
    with open(writepath,"w") as writefile:
        writefile.writelines(contents)


# file_to_edit="./codestuff.c"
# parse_mergefile(file_to_edit, MERGE_FILE_PATH)


def main(camera_dir, codefile_path):
    imageProcessing.parseAll(camera_dir)
    for filename in os.listdir("C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\text"):
        try:
            file_path = os.path.join("C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\text", filename)
            OCRText.getText(file_path, 
                    "C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\ocr.txt")
        except Exception as e:
            print(e)
            continue
    
    generateMergeFile.generateToMerge("C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\ocr.txt", 
                                      "C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\images",
                                      "C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\tomerge.txt")
    
    parse_mergefile(codefile_path, "C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\tomerge.txt")


main("C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\annotations", "C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\royIQ.py")
# parse_mergefile("C:\\Users\\zroy1\\SE101\\se101-team-21\\utils\\royIQ.py", "C:\\Users\\zroy1\\SE101\\se101-team-21\\utils\\tomerge.txt")
