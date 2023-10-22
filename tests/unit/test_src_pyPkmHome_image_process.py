import cv2
import numpy as np
import pytesseract
import pytest
from PIL import Image

from src.pyPkmHome.image_process import *  # replace with the actual module name


def test_extractText():
    # Create a 2x2 image with two colors: black and white
    img = np.array(
        [[[0, 0, 0], [255, 255, 255]], [[0, 0, 0], [255, 255, 255]]], dtype=np.uint8
    )

    # TODO: dummy expected
    # The expected text extracted from the image
    expected = ""

    # Call the function with the test image
    result = extractText(img)

    # Assert that the result is as expected
    assert result == expected

    # Test with None input
    with pytest.raises(ValueError):
        extractText(None)

    # Test with an invalid crop rectangle
    with pytest.raises(ValueError):
        extractText(img, crop_rect=(0, 0, 3, 3))

    # Test with an invalid crop rectangle data type
    with pytest.raises(ValueError):
        extractText(img, crop_rect=(0.1, 0.1, 1.1, 1.1))


def test_extractColorHex():
    # Create a 3x3 image with two colors: black and white
    img = np.array(
        [
            [[0, 0, 0], [255, 255, 255], [255, 255, 255]],
            [[0, 0, 0], [255, 255, 255], [255, 255, 255]],
            [[0, 0, 0], [255, 255, 255], [255, 255, 255]],
        ],
        dtype=np.uint8,
    )

    # Revert Image color
    revert_img = 255 - img

    # The expected color hex code for white
    expected = "#ffffff"

    # Call the function with the test image
    result = extractColorHex(revert_img)

    # Assert that the result is as expected
    assert result == expected

    # Test with None input
    with pytest.raises(ValueError):
        extractColorHex(None)

    # Test with an image of one color
    img_one_color = np.array(
        [[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]], dtype=np.uint8
    )
    with pytest.raises(ValueError):
        extractColorHex(img_one_color)


def test_searchImage():
    # Create a random image of size 300x300
    main_image = np.random.randint(0, 256, (300, 300), dtype=np.uint8)

    # Create a random image of size 50x50 as the template image
    template_image = np.random.randint(0, 256, (50, 50), dtype=np.uint8)

    # Place the template_image in the center of the main_image
    main_image[125:175, 125:175] = template_image

    # Test that searchImage can find the template in the main image
    assert searchImage(template_image, main_image)

    # Test that searchImage cannot find a non-existent template
    non_existent_template = np.random.randint(0, 256, (60, 60), dtype=np.uint8)
    assert not searchImage(non_existent_template, main_image)

    # Test that searchImage can find the template in a cropped region of the main image
    assert searchImage(template_image, main_image, crop_rect=(100, 100, 200, 200))

    # Test that searchImage cannot find the template outside the cropped region
    assert not searchImage(template_image, main_image, crop_rect=(0, 0, 100, 100))

    # Test ValueError when main_image is None
    with pytest.raises(ValueError):
        searchImage(template_image, None)

    # Test ValueError when template_image is None
    with pytest.raises(ValueError):
        searchImage(None, main_image)

    # Test ValueError when crop_rect is not a tuple of four integers
    with pytest.raises(ValueError):
        searchImage(template_image, main_image, crop_rect=(0, 0, 0))

    # Test ValueError when threshold is not a float between 0 and 1
    with pytest.raises(ValueError):
        searchImage(template_image, main_image, threshold=1.5)
