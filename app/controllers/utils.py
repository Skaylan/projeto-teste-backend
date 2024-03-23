import os
import sys
import base64
import cv2
from uuid import uuid4

def print_error_details(error: Exception) -> None:
    """
    Print error details for the given exception.
    Args:
        error (Exception): The exception for which error details will be printed.
    Returns:
        None
    """
    
    print(f'error class: {error.__class__} | error cause: {error.__cause__}')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


def convert_base64_to_image(img_base64_string: str, image_uuid: str, save_path: str) -> bool:
    """
    Converts a base64 encoded image to a PNG file and saves it to the specified path.

    Args:
        img_base64_string (str): The base64 encoded image string.
        image_uuid (str): The unique identifier for the image.
        save_path (str): The path where the image file will be saved.

    Returns:
        bool: True if the image was successfully saved, False otherwise.
    """
    
    try:
        img_data = base64.b64decode(img_base64_string)
        filename = f'{image_uuid}.jpeg'
        with open(f'{save_path}/{filename}', 'wb') as f:
            f.write(img_data)
        return True
    except Exception as error:
        print_error_details(error)
        return False

def convert_image_to_base64(img_path: str, img_uuid: str) -> str:
    """
    Function to convert an image to base64 format.

    Args:
        img_path (str): The path to the image file.
        img_uuid (str): The unique identifier for the image.

    Returns:
        str: The base64 encoded string of the image.
    """

    with open(f'{img_path}//{img_uuid}.jpeg', 'rb') as img_file:
        base64_string = base64.b64encode(img_file.read())
    return str(base64_string)[2:].replace("'", '')


    
def compress_image(file_name: str, file_path: str):
    """
    Compresses an image file.

    Parameters:
    file_name (str): The name of the image file.
    file_path (str): The path to the image file.

    Returns:
    None
    """
    try:
        img = cv2.imread(f'{file_path}/{file_name}.jpeg')
        cv2.imwrite(f'{file_path}/{file_name}.jpeg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        
    except Exception as error:
        print_error_details(error)
        return