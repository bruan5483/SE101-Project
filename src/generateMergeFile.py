import re
import os

# TOMERGE_PATH = "utils\\tomerge.txt"

def parseOCR(ocr_file, tomerge_path):
    # list in the form [line number, comment]
    changes =  []
    with open(ocr_file, 'r+') as file:
        lines = file.readlines()
        for line in lines:
            print(line.strip())
            # line number 
            number = re.match(r'^[^\w]*\s*(\d+)\)*', line.strip())
            if number:
                number = number.group(1)
            else:
                number = 1
            # body of text 
            comment = re.search(r'[^\w]*\s*\d+\)*\s*(.*?)(\))*$', line.strip())
            if comment:
                changes.append([number, comment.group(1)])
    
    # save changes 
    new_lines = []
    for change in changes:
        new_lines.append(f"{change[0]},-1,[comment] {change[1]}[newline]\n")

    with open(tomerge_path, 'a') as file: # change path 
        file.writelines(new_lines)


def parseImage(directory, tomerge_path):
    LINES_PER_IMG = 35
    images = []
    # grab path of all images in directory
    for filename in os.listdir(directory):
        try:
            file_path = os.path.join(directory, filename)
            images.append(file_path)
        except Exception as e:
            continue
    images.sort()

    # modify in format line number, index 0, path
    for i in range(len(images)):
        line = (int(images[i].split("_")[-1].split(".")[0]) * LINES_PER_IMG) + 1 + i
        images[i] = f"{line},0,[comment] {images[i]}[newline]\n"

    # save changes 
    with open(tomerge_path, 'a') as file: # change path 
        file.writelines(images)

# main 
def generateToMerge(ocr_file, img_directory, tomerge_path):
    parseOCR(ocr_file, tomerge_path)
    parseImage(img_directory, tomerge_path)
    return tomerge_path

# change paths 
# generateToMerge("C:\\Users\\zroy1\\SE101\\se101-team-21\\utils\\ocr.txt", 
#                 "C:\\Users\\zroy1\\SE101\\se101-team-21\\utils\\codeImages",
#                 TOMERGE_PATH)

