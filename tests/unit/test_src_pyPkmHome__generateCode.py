import os
from unittest.mock import call, mock_open, patch

import pytest

from src.pyPkmHome._generateCode import *


def test_createRetangleDict():
    # Define the input and expected output
    raw = {
        "pokemon_HOME": {
            "crop_rectangle": {
                "nature_stat": {
                    "var": "nature_stat",
                    "desc": "Nature and Stat",
                    "type_hint": "dict",
                    "attack": {
                        "desc": "Stat",
                        "stat": "Attack",
                        "x1": 0,
                        "y1": 0,
                        "x2": 100,
                        "y2": 100,
                    },
                }
            }
        }
    }
    filter = ["nature_stat"]
    expected_output = {
        "nature_stat": {
            "Attack": ["Stat", (0, 0, 100, 100)],
            "desc": "Nature and Stat",
            "type_hint": "dict",
        }
    }

    # Call the function with the test input
    result = createRetangleDict(raw, filter)

    # Assert that the function output matches the expected output
    assert result == expected_output


def test_extractDict():
    # Define the input and expected output
    raw = {
        "pokemon_HOME": {
            "const": {
                "crop rectangle disabled": {
                    "var": "CROP_RECT_FALSE",
                    "desc": "Constant for a false crop rectangle",
                    "type_hint": "tuple",
                    "value": (0, 0, 0, 0),
                },
            },
        }
    }
    expected_output = {
        "CROP_RECT_FALSE": {
            "desc": "Constant for a false crop rectangle",
            "type_hint": "tuple",
            "val": (0, 0, 0, 0),
        }
    }

    # Call the function with the test input
    result = extractDict(raw)

    # Assert that the function output matches the expected output
    assert result == expected_output


def test_mainFunction():
    # Define the input and expected output
    raw = {
        "pokemon_HOME": {
            "crop_rectangle": {
                "nature_stat": {
                    "var": "nature_stat",
                    "desc": "Nature and Stat",
                    "type_hint": "dict",
                    "attack": {
                        "desc": "Stat",
                        "stat": "Attack",
                        "x1": 0,
                        "y1": 0,
                        "x2": 100,
                        "y2": 100,
                    },
                },
                "stat_iv": {
                    "var": "stat_iv",
                    "desc": "S",
                    "type_hint": "dict",
                    "attack": {
                        "desc": "Stat",
                        "stat": "Attack",
                        "x1": 0,
                        "y1": 0,
                        "x2": 100,
                        "y2": 100,
                    },
                },
                "main_img_based": {
                    "var": "stat_iv",
                    "desc": "S",
                    "type_hint": "dict",
                    "attack": {
                        "desc": "Stat",
                        "stat": "Attack",
                        "x1": 0,
                        "y1": 0,
                        "x2": 100,
                        "y2": 100,
                    },
                },
                "main_txt_based": {
                    "var": "stat_iv",
                    "desc": "S",
                    "type_hint": "dict",
                    "attack": {
                        "desc": "Stat",
                        "stat": "Attack",
                        "x1": 0,
                        "y1": 0,
                        "x2": 100,
                        "y2": 100,
                    },
                },
            },
            "const": {
                "crop rectangle disabled": {
                    "var": "CROP_RECT_FALSE",
                    "desc": "Constant for a false crop rectangle",
                    "type_hint": "tuple",
                    "value": (0, 0, 0, 0),
                },
            },
        }
    }
    expected_output = """# This is a generated Python script
from typing import Any, Tuple, Dict
# Nature and Stat
nature_stat:  dict = {
    # Stat
    "Attack": (0, 0, 100, 100),
}
# S
stat_iv:  dict = {
    # Stat
    "Attack": (0, 0, 100, 100),
}
# Constant for a false crop rectangle
CROP_RECT_FALSE: tuple = (0, 0, 0, 0)

################################################################################
#                                END OF FILE                                   #
################################################################################"""

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


# Run the test
pytest.main(["-v"])
