# Import the libraries
from typing import Tuple

import cv2
import numpy
import pytesseract
from PIL import Image

from src._CONST_ import *
from ._CONST_ import *

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)


def extractText(
    main_image: numpy.ndarray,
    crop_rect: Tuple[int, int, int, int] = CROP_RECT_FALSE,
    scale_factor: float = SCALE_FACTOR,
) -> str:
    """Extract text from an image using OCR.

    Parameters:
    main_image: The image file from which to extract the text.
    crop_rect: A tuple of four integers (x1, y1, x2, y2) that defines the cropping rectangle for the main image. The default value is (0, 0, 0, 0), which means no cropping.
    scale_factor: A float value that defines the factor by which to resize the image before text extraction. The default value is 2.0.

    Returns:
    A string that represents the extracted text from the image.
    """

    # Check if main_image is None
    if main_image is None:
        raise ValueError("main_image cannot be None")

    # Check if crop_rect is a tuple of four integers and within the bounds of the main image
    if (
        not isinstance(crop_rect, tuple)
        or len(crop_rect) != len(CROP_RECT_FALSE)
        or not all(isinstance(i, int) for i in crop_rect)
    ):
        raise ValueError("crop_rect must be a tuple of four integers")

    x1, y1, x2, y2 = crop_rect
    if (
        x1 < INT_ZERO
        or y1 < INT_ZERO
        or x2 > main_image.shape[SECOND_ELEMENT]
        or y2 > main_image.shape[FIRST_ELEMENT]
    ):
        raise ValueError("crop_rect is out of bounds")

    # If a crop rectangle is provided, crop the main image
    if crop_rect != CROP_RECT_FALSE:
        main_image = main_image[y1:y2, x1:x2]

    # Resize the image by the specified scale factor
    main_image = cv2.resize(main_image, None, fx=scale_factor, fy=scale_factor)

    # Convert the resized image to grayscale
    gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blur = cv2.GaussianBlur(gray, GAUSSIAN_KERNEL_SIZE, GAUSSIAN_SIGMA_X)

    # Apply Otsu's thresholding to the blurred image
    _, thresh_img = cv2.threshold(
        blur,
        THRESHOLD_THRESH,
        THRESHOLD_MAXVAL,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    # Perform morphological operations (dilation followed by erosion) on the thresholded image
    kernel = numpy.ones(NUMPY_ONES_SHAPES, numpy.uint8)
    morph_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel)

    # Invert the colors of the morphological image
    morph_img = INT_TWO_FIVE_FIVE - morph_img

    # Apply denoising to the inverted image
    denoised_img = cv2.fastNlMeansDenoising(
        morph_img,
        h=DENOISE_FILTER_STRENGTH,
        templateWindowSize=DENOISE_TEMPLATE_SIZE,
        searchWindowSize=DENOISE_TEMPLATE_SEARCH,
    )

    # Convert the denoised OpenCV image (numpy array) back to a PIL image
    img = Image.fromarray(denoised_img)

    # Use Pytesseract to extract text from the PIL image
    text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")

    return text


def extractColorHex(img: numpy.ndarray) -> str:
    """Extract the color hex code of the text in an image.

    Parameters:
    img: The image file from which to extract the color.

    Returns:
    A string that represents the color hex code of the text in the image.
    """

    if img is None:
        raise ValueError("img cannot be None")

    # Create an image object from the input array using Pillow library
    im = Image.fromarray(img)

    # Sort the colors in the image by frequency
    colors = sorted(im.getcolors())

    # Check if there are at least two colors in the image
    if len(colors) < INT_TWO:
        raise ValueError(
            "The image does not have enough colors to extract a color hex code"
        )

    # Get the second most frequent color (the most frequent is usually the background)
    # Convert the RGB values to a hexadecimal color code
    color_hex = "#%02x%02x%02x" % colors[SECOND_LAST_ELEMENT][SECOND_ELEMENT]

    return color_hex


def searchImage(
    template_image: numpy.ndarray,
    main_image: numpy.ndarray,
    crop_rect: Tuple[int, int, int, int] = CROP_RECT_FALSE,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Search for a template image in a main image and return True if found, False otherwise.

    Parameters:
    template_image: The image file of the template to be searched.
    main_image: The image file of the main image where the template is searched.
    crop_rect: A tuple of four integers (x1, y1, x2, y2) that defines the cropping rectangle for the main image. The default value is (0, 0, 0, 0), which means no cropping.
    threshold: A float value between 0 and 1 that defines the minimum matching score to consider a match. The default value is 0.8.

    Returns:
    A boolean value that indicates whether the template image is found in the main image or not.
    """

    if main_image is None:
        raise ValueError("main_image cannot be None")
    if template_image is None:
        raise ValueError("template_image cannot be None")

    if (
        not isinstance(crop_rect, tuple)
        or len(crop_rect) != len(CROP_RECT_FALSE)
        or not all(isinstance(i, int) for i in crop_rect)
    ):
        raise ValueError("crop_rect must be a tuple of four integers")

    if not isinstance(threshold, float) or not INT_ZERO <= threshold <= INT_ONE:
        raise ValueError("threshold must be a float between 0 and 1")

    # Check if crop_rect is within the bounds of the main image
    x1, y1, x2, y2 = crop_rect
    if (
        x1 < INT_ZERO
        or y1 < INT_ZERO
        or x2 > main_image.shape[SECOND_ELEMENT]
        or y2 > main_image.shape[FIRST_ELEMENT]
    ):
        raise ValueError("crop_rect is out of bounds")

    # If crop_rect is not default value (0,0,0,0), crop the main image according to the given coordinates
    if crop_rect != CROP_RECT_FALSE:
        main_image = main_image[y1:y2, x1:x2]

    match_result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)

    return numpy.any(match_result >= threshold)


################################################################################
#                                END OF FILE                                   #
################################################################################
