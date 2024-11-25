from PIL import Image
import os

# from logger_config import log_function_calls
# from logger_config import setup_logger

# setup_logger()

# Converts jpg to png
# @log_function_calls()
def jpgToPng(image):
    if os.path.splitext(image)[1] == ".png": return image

    img = Image.open(image)

    newImage = os.path.splitext(image)[0] + ".png"
    img.save(newImage, "png")

    os.remove(image)

    return newImage

# Parses image by red and blue pixels
# @log_function_calls()
def parseImage(image, index):
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(image)))
    folderRed = os.path.join(baseDir, "text")
    folderBlue = os.path.join(baseDir, "images")
    
    try:
        # print(f"\nimagE:{image}\n")
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
                if (r >= 120 and r > g and r > b and (r-b) >= 20): redParse[i,j] = (0, 0, 0)

                else: redParse[i,j] = (255, 255, 255)
                
                # Isolate blue
                if (b >= 95 and b > g and b > r and (b-r) >= 20): blueParse[i,j] = (0, 0, 0)

                else: blueParse[i,j] = (255, 255, 255)
        
        # print(os.path.join(folderRed, "img_{}.png".format(index)))

        inputImageR.save(os.path.join(folderRed, "img_{}.png".format(index)))
        inputImageB.save(os.path.join(folderBlue, "img_{}.png".format(index)))

    except: return

# Parses all images in the images directory
# @log_function_calls()
def parseAll(dir):
    for index, file in enumerate(os.listdir(dir)):

        try:
            filePath = os.path.join(dir, file)
            # print(filePath) 
            if os.path.isfile(filePath):
                if (os.path.splitext(filePath)[1] != ".png"): 
                    filePath = jpgToPng(filePath)

            parseImage(filePath, index)
        
        except: continue

# removes all current images in the image dir
# @log_function_calls()
def pruneDir(dir_path):
    for fname in os.listdir(dir_path):
        file_path = os.path.join(dir_path, fname)
        os.remove(file_path)


# checks if an index is valid in the images dir
# @log_function_calls()
def validateImageIndex(images_dir, index) -> int:
    n = len(os.listdir(images_dir))

    return  max(0, min(n-1, index))

# parseAll("C:\\Users\\zroy1\\SE101\\se101-team-21\\utils\\annotations")
