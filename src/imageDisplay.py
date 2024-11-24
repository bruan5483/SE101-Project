import cv2  # Install with: pip install opencv-python

from logger_config import log_function_calls
from logger_config import setup_logger

setup_logger()

@log_function_calls()
def display_fullscreen_image(image_path):

    # Read the image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        return

    # Create a named window and set it to fullscreen
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()  # Close the window
