from google.cloud import vision
import os


# from logger_config import log_function_calls
# from logger_config import setup_logger

# setup_logger()

# @log_function_calls()
def getText(path, output_file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ronak/Desktop/project-code/utils/google_ocr_service_token.json"

    
    client = vision.ImageAnnotatorClient()
    

    with open(path, "rb") as image_file:
        content = image_file.read()
 
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    with open(output_file, "a", encoding='utf-8') as f:  # Open the output file to write detected text
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

# getText("utils\\text\\img_0.png", "utils\\ocr.txt")
