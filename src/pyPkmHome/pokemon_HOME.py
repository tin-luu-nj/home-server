# Import the libraries
import os
from typing import Dict, Tuple

import cv2
import numpy
import pytesseract

from src._CONST_ import *
from ._CONST_ import *
from .image_process import *

# TODO: [Testing] export image with check areas
# TODO: [Development] check area without cropping image

# Create a dictionary of template images for icons
TEMPLATE_PATH = "data/Pkm_HOME/template/"
TEMPLATE_IMG = {
    # Read the image file for the male icon
    "male": cv2.imread(TEMPLATE_PATH + "male_icon.png"),
    # Read the image file for the female icon
    "female": cv2.imread(TEMPLATE_PATH + "female_icon.png"),
    # Read the image file for the minus icon for stats
    "stats_minus": cv2.imread(TEMPLATE_PATH + "stats_minus_icon.png"),
    # Read the image file for the plus icon for stats
    "stats_plus": cv2.imread(TEMPLATE_PATH + "stats_plus_icon.png"),
}


def extractNatureStats(main_image: numpy.ndarray) -> str:
    """Extract the nature and stats of a Pokemon from an image.

    Parameters:
    main_image: The image file from which to extract the nature and stats.
    TEMPLATE_IMG: A dictionary that contains the template images for the minus and plus icons.
    CROP_RECT_NATURE_STAT: A dictionary that contains the cropping rectangles for each stat.

    Returns:
    A string that represents the nature and stats of the Pokemon in the image.
    """

    # Check if main_image is None
    if main_image is None:
        raise ValueError("main_image cannot be None")

    nature_stat = []

    # Loop through the template images
    for template in [TEMPLATE_IMG["stats_minus"], TEMPLATE_IMG["stats_plus"]]:
        # Loop through the keys and values of the cropping rectangle dictionary
        for key, value in CROP_RECT_NATURE_STAT.items():
            # Check if the icon is found in the main image within the cropping rectangle
            if searchImage(template, main_image, value):
                # If yes, append the corresponding stat to the nature_stat list
                nature_stat.append(key)

    # If the nature_stat list is empty, it means the nature is neutral
    if not nature_stat:
        nature_stat = NATURE_NEUTRAL
    # If the nature_stat list has two elements, it means the nature has a plus and a minus stat
    else:
        # Format the nature_stat as a string with a minus and a plus sign
        nature_stat = NATURE_MINUS + nature_stat[0] + NATURE_PLUS + nature_stat[1]

    return nature_stat


def extractStatsIV(main_image: numpy.ndarray) -> Dict[str, str]:
    """Extract the Individual Values (IVs) of a Pokemon's stats from an image.

    Parameters:
    main_image: The image file from which to extract the stats.

    Returns:
    A dictionary where the keys are the stat names and the values are the extracted IVs.
    """

    # Check if main_image is None
    if main_image is None:
        raise ValueError("main_image cannot be None")

    stats_IV = {}

    # Loop through the keys and values of the cropping rectangle dictionary
    for key, value in CROP_RECT_STAT_IV.items():
        # Extract the text from the main image within the cropping rectangle
        text = extractText(main_image, value)

        # Remove newline characters from the extracted text and store it in the dictionary
        stats_IV[key] = text.replace("\n", "")

    return stats_IV


def extractMain(main_image: numpy.ndarray) -> Dict[str, str]:
    """Extract the main text-based information from an image.

    Parameters:
    main_image: The image file from which to extract the information.
    CROP_RECT_MAIN_TXT_BASED: A dictionary that contains the cropping rectangles for each piece of information.

    Returns:
    A dictionary where the keys are the names of the pieces of information and the values are the extracted texts.
    """

    # Check if main_image is None
    if main_image is None:
        raise ValueError("main_image cannot be None")

    main_txt_based = {}

    # Loop through the keys and values of the cropping rectangle dictionary
    for key, value in CROP_RECT_MAIN_TXT_BASED.items():
        # Extract the text from the main image within the cropping rectangle
        text = extractText(main_image, value)

        # Remove newline characters from the extracted text and store it in the dictionary
        main_txt_based[key] = text.replace("\n", "")

    return main_txt_based


def extractGender(main_image: numpy.ndarray) -> str:
    """Extract the gender of a Pokemon from an image.

    Parameters:
    main_image: The image file from which to extract the gender.

    Returns:
    A string that represents the gender of the Pokemon in the image.
    """

    # Initialize gender as "GENDERLESS"
    gender = GENDER_GENDERLESS

    # Loop through the keys of the template images
    for key in [GENDER_MALE, GENDER_FEMALE]:
        # Check if the gender icon is found in the main image within the cropping rectangle
        if searchImage(
            TEMPLATE_IMG[key], main_image, CROP_RECT_MAIN_IMG_BASED["Gender"]
        ):
            # If yes, set gender to the corresponding gender
            gender = key

    return gender


# Define the main function of the program
def mainFunction():
    """Main function to extract Pokemon information from images in a specified folder.

    This function loops through each image file in the specified folder, extracts various pieces of Pokemon information from each image using different functions, and appends the extracted information to a text file.
    """

    print("[1] Attempting to initialize...")
    # Get all the image files in the data folder
    folder = "data/Pkm_HOME/"
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    # Loop through each image file
    for file in files:
        # Load the image of a Pokemon summary screen
        main_image = cv2.imread(folder + file)
        # Extract the Pokemon information from the image using different functions
        stats_IV = extractStatsIV(main_image)
        nature_stat = extractNatureStats(main_image)
        gender = extractGender(main_image)
        main = extractMain(main_image)
        # Store the Pokemon information in a list
        pkm = [
            main["No."],
            main["Species"],
            gender,
            main["Lv."],
            main["Nature"],
            nature_stat,
            main["Held Item"],
            main["Ability"],
            stats_IV["HP"],
            stats_IV["Attack"],
            stats_IV["Defense"],
            stats_IV["Sp.Atk"],
            stats_IV["Sp.Def"],
            stats_IV["Speed"],
            main["Stat Judge"],
            main["Move_1"],
            main["Move_2"],
            main["Move_3"],
            main["Move_4"],
            main["OT"],
            main["TID"],
        ]
        # Append the Pokemon information to a text file
        with open("out/pkm_home.txt", "a") as outfile:
            print(pkm)
            outfile.write(",".join(str(i) for i in pkm))
            outfile.write("\n")


################################################################################
#                                END OF FILE                                   #
################################################################################
