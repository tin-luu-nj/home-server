import os

import cv2
import numpy as np
import pytest

from src.pyPkmHome.pokemon_HOME import *  # replace with the actual module name


def test_001_F_extractNatureStats(monkeypatch):
    # Prepare the inputs
    main_image = np.random.rand(100, 100, 3)  # replace with an actual image

    # Define a mock searchImage function to return True if the nature is neutral
    def mock_searchImage(template_img, main_img, rect):
        return True

    # Replace the real searchImage function with the mock function
    monkeypatch.setattr("src.pyPkmHome.pokemon_HOME.searchImage", mock_searchImage)

    # Call the function with the inputs
    result = extractNatureStats(main_image)

    # Assert the expected outputs
    assert isinstance(result, str), "The result should be a string"
    assert result in [
        NATURE_NEUTRAL,
        NATURE_MINUS + "Attack" + NATURE_PLUS + "Defense",
    ], "The result is not as expected"


# This test checks if the function raises a ValueError when main_image is None
def test_002_F_extractNatureStats_with_None():
    with pytest.raises(ValueError):
        extractNatureStats(None)


def test_003_F_extractStatsIV(monkeypatch):
    # Define a mock image as a numpy array
    mock_image = np.array([[255, 255, 255], [255, 255, 255], [255, 255, 255]])

    # Define a mock CROP_RECT_STAT_IV dictionary
    mock_CROP_RECT_STAT_IV = {"HP": (0, 0, 1, 1), "Attack": (1, 1, 2, 2)}

    # Define a mock extractText function to return the key name
    def mock_extractText(image, rect):
        for key, value in mock_CROP_RECT_STAT_IV.items():
            if value == rect:
                return key
        return ""

    # Replace the real extractText function with the mock function
    monkeypatch.setattr("src.pyPkmHome.pokemon_HOME.extractText", mock_extractText)

    # Call the function with the mock image
    result = extractStatsIV(mock_image)

    # Check that the result is as expected
    assert result == {
        "HP": "",
        "Attack": "",
        "Defense": "",
        "Sp.Atk": "",
        "Sp.Def": "",
        "Speed": "",
    }


def test_004_F_extractStatsIV_no_image():
    # Call the function with None as the image
    with pytest.raises(ValueError):
        extractStatsIV(None)


def test_005_F_extractMain(monkeypatch):
    # Define a mock image as a numpy array
    mock_image = np.array([[255, 255, 255], [255, 255, 255], [255, 255, 255]])

    # Define a mock CROP_RECT_MAIN_TXT_BASED dictionary
    mock_CROP_RECT_MAIN_TXT_BASED = {"Name": (0, 0, 1, 1), "Type": (1, 1, 2, 2)}

    # Define a mock extractText function to return the key name
    def mock_extractText(image, rect):
        for key, value in mock_CROP_RECT_MAIN_TXT_BASED.items():
            if value == rect:
                return key
        return ""

    # Replace the real extractText function with the mock function
    monkeypatch.setattr("src.pyPkmHome.pokemon_HOME.extractText", mock_extractText)

    # Call the function with the mock image
    result = extractMain(mock_image)

    # Check that the result is as expected
    assert result == {
        "No.": "",
        "Species": "",
        "Lv.": "",
        "Move_1": "",
        "Move_2": "",
        "Move_3": "",
        "Move_4": "",
        "OT": "",
        "TID": "",
        "Nature": "",
        "Ability": "",
        "Held Item": "",
        "Stat Judge": "",
    }


def test_006_F_extractMain_no_image():
    # Call the function with None as the image
    with pytest.raises(ValueError):
        extractMain(None)


def test_007_F_extractGender(monkeypatch):
    # TODO: Dummy test, need accurate input and output
    # Define a mock image as a numpy array
    mock_image = np.array([[255, 255, 255], [255, 255, 255], [255, 255, 255]])

    # Define a mock CROP_RECT_MAIN_IMG_BASED dictionary
    mock_CROP_RECT_MAIN_IMG_BASED = {"Gender": (0, 0, 1, 1)}

    # Define a mock TEMPLATE_IMG dictionary
    mock_TEMPLATE_IMG = {
        GENDER_MALE: np.array([[0, 0], [0, 0]]),
        GENDER_FEMALE: np.array([[0, 0], [0, 0]]),
    }

    # Define a mock searchImage function to return True if the key is GENDER_MALE
    def mock_searchImage(template_img, main_img, rect):
        for key, value in mock_TEMPLATE_IMG.items():
            if np.array_equal(value, template_img):
                return key == GENDER_MALE
        return False

    # Replace the real searchImage function with the mock function
    monkeypatch.setattr("src.pyPkmHome.pokemon_HOME.searchImage", mock_searchImage)

    # Call the function with the mock image
    result = extractGender(mock_image)

    # Check that the result is as expected
    assert result == GENDER_GENDERLESS


def test_008_F_extractGender_no_image():
    # Call the function with None as the image
    with pytest.raises(ValueError):
        extractGender(None)


def test_009_F_mainFunction(monkeypatch):
    # TODO: Dummy Test, need real input and output
    # Define a mock image as a numpy array
    mock_image = np.array([[255, 255, 255], [255, 255, 255], [255, 255, 255]])

    # Define a mock os.listdir function to return a list of files
    def mock_os_listdir(folder):
        return ["file1.png", "file2.png"]

    # Replace the real os.listdir function with the mock function
    monkeypatch.setattr(os, "listdir", mock_os_listdir)

    # Define a mock cv2.imread function to return the mock image
    def mock_cv2_imread(file):
        return mock_image

    # Replace the real cv2.imread function with the mock function
    monkeypatch.setattr(cv2, "imread", mock_cv2_imread)

    # Define a mock extractStatsIV function to return a dictionary of stats
    def mock_extractStatsIV(image):
        return {
            "HP": "100",
            "Attack": "100",
            "Defense": "100",
            "Sp.Atk": "100",
            "Sp.Def": "100",
            "Speed": "100",
        }

    # Replace the real extractStatsIV function with the mock function
    monkeypatch.setattr(
        "src.pyPkmHome.pokemon_HOME.extractStatsIV", mock_extractStatsIV
    )

    # Define other mock functions for extractNatureStats, extractGender, and extractMain here...

    # Call the mainFunction
    mainFunction()

    # Check that the output file exists and contains the expected content
    with open("out/pkm_home.txt", "r") as outfile:
        lines = outfile.readlines()
        assert len(lines) == 670
        assert (
            lines[0]
            == "No. 0001,Bulbasaur,MALE,Lv. 14,Bold,-Attack/+Defense,None,Overgrow,Fantastic,Fantastic,Fantastic,Fantastic,Fantastic,Fantastic,Amazing stats!,Vine Whip,Growth,Leech Seed,Razor Leaf,HOME,210601\n"
        )
