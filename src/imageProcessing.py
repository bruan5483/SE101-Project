from PIL import Image
import os

# Converts jpg to png
def jpgToPng(image):
    if os.path.splitext(image)[1] == ".png": return image

    img = Image.open(image)

    newImage = os.path.splitext(image)[0] + ".png"
    img.save(newImage, "png")

    os.remove(image)

    return newImage

# Parses image by red and blue pixels
def parseImage(image):
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(image)))
    folder = os.path.join(baseDir, "processedImages")

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
            if (b < 50): redParse[i,j] = (0, 0, 0)

            else: redParse[i,j] = (255, 255, 255)
            
            # Isolate blue
            if (r < 110): blueParse[i,j] = (0, 0, 0)

            else: blueParse[i,j] = (255, 255, 255)

    inputImageR.save(os.path.join(folder, "{}_parsedR.png".format(os.path.splitext(os.path.basename(image))[0])))
    inputImageB.save(os.path.join(folder, "{}_parsedB.png".format(os.path.splitext(os.path.basename(image))[0])))
    inputImageR.show()
    inputImageB.show()

# Parses all images in the images directory
def parseAll(dir):
    for file in os.listdir(dir):
        filePath = os.path.join(dir, file)

        if os.path.isfile(filePath):
            if (os.path.splitext(filePath)[1] != ".png"): 
                filePath = jpgToPng(filePath)

            parseImage(filePath)


# removes all current images in the image dir
def pruneDir(dir_path):
    for fname in os.listdir(dir_path):
        file_path = os.path.join(dir_path, fname)
        os.remove(file_path)


# checks if an index is valid in the images dir
def validateImageIndex(images_dir, index) -> int:
    n = len(os.listdir(images_dir))

    return  max(0, min(n-1, index))