from google.cloud import vision

def get_text(path, output_file):
    
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    with open(output_file, "w") as f:  # Open the output file to write detected text
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = "".join([symbol.text for symbol in word.symbols])
                        f.write(f"{word_text} ")

                    f.write("\n")  # Add a newline after each paragraph

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

# Example
get_text(
    "/Users/bryant.ruan/Desktop/SE101/SE101-Project/se101-team-21/SE101_OCR/images/IMG_0029.jpg",
    "/Users/bryant.ruan/Desktop/SE101/SE101-Project/se101-team-21/SE101_OCR/images/detected_text.txt"
)
