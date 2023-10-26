from unittest.mock import mock_open, patch
import yaml, json

from src.pyPkmHome._generateCode import *
import pytest


@pytest.fixture
def raw_loading():
    with open(
        "tests/unit/database/src_pyPkmHome/_generateCode_fixture.yaml", "r"
    ) as _file:
        raw = yaml.safe_load(_file)

    from .database.src_pyPkmHome._generateCode_expected_output import (
        test_001_expected_output,
        test_002_expected_output,
    )

    return raw, test_001_expected_output, test_002_expected_output


def test_001_F_createRetangleDict(raw_loading):
    # Define the input and expected output
    raw, expected_output, _ = raw_loading
    filter = ["nature_stat", "stat_iv", "main_img_based", "main_txt_based"]

    # Call the function with the test input
    result = createRetangleDict(raw, filter)

    # Assert that the function output matches the expected output
    assert result == expected_output


def test_002_F_extractDict(raw_loading):
    # Define the input and expected output
    raw, _, expected_output = raw_loading

    # Call the function with the test input
    result = extractDict(raw)

    # Assert that the function output matches the expected output
    assert result == expected_output


def test_003_F_mainFunction(raw_loading):
    # Define the input and expected output
    raw, _, _ = raw_loading

    with open(
        "tests/unit/database/src_pyPkmHome/_generateCode_test_003_expected_output.py"
    ) as file_:
        expected_output = file_.read()

    # Mock template
    with open("src/pyPkmHome/_CONST_template.txt") as file_:
        m = mock_open(read_data=file_.read())

    # Mock open function calls
    with patch("builtins.open", m):
        mainFunction(raw)

    # Check that the template file was read
    m.assert_any_call("src/pyPkmHome/_CONST_template.txt")

    # Check that the output file was written with the expected content
    m.assert_any_call("src/pyPkmHome/_CONST_.py", "w")
    m().write.assert_called_once_with(expected_output)
