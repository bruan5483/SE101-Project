from PIL import Image
import os

def jpgToPng(image):
    if os.path.splitext(image)[1] == ".png": return image

    img = Image.open(image)

    newImage = os.path.splitext(image)[0] + ".png"
    img.save(newImage, "png")

    os.remove(image)

    return newImage


def parseImage(image):
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(image)))
    folderRed = os.path.join(baseDir, "text")
    folderBlue = os.path.join(baseDir, "images")
    folderFile = os.path.join(baseDir, "files")

    try:
        inputImageR = Image.open(image)
        inputImageB = inputImageR.copy()

        inputImageR = inputImageR.convert("RGB")
        inputImageB = inputImageB.convert("RGB")

        redParse = inputImageR.load()
        blueParse = inputImageB.load()

        width, height = inputImageR.size

        for i in range(width):
            for j in range(height):

                r, g, b = inputImageR.getpixel((i,j))

                # Isolate red
                if (r >= 90 and r > g and r > b and (r-b) >= 35): redParse[i,j] = (0, 0, 0)

                else: redParse[i,j] = (255, 255, 255)
                
                # Isolate blue
                if (b >= 30 and b > g and b > r): blueParse[i,j] = (0, 0, 0)

                else: blueParse[i,j] = (255, 255, 255)
        
        inputImageR.save(os.path.join(folderRed, os.path.basename(image)))
        inputImageB.save(os.path.join(folderBlue, os.path.basename(image)))
        inputImageB.save(os.path.join(folderFile, os.path.basename(image)))

    except: return

def parseAll(dir):
    for file in os.listdir(dir):

        try:
            filePath = os.path.join(dir, file)
            if os.path.isfile(filePath):
                if (os.path.splitext(filePath)[1] != ".png"): 
                    filePath = jpgToPng(filePath)

            parseImage(filePath)
        
        except: continue

def pruneDir(dir_path):
    for fname in os.listdir(dir_path):
        file_path = os.path.join(dir_path, fname)
        os.remove(file_path)


def validateImageIndex(images_dir, index) -> int:
    n = len(os.listdir(images_dir))

    return  max(0, min(n-1, index))

# parseAll("C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\annotations")
