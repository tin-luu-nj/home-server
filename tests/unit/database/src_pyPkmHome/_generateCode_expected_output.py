test_001_expected_output = {
    "CROP_RECT_NATURE_STAT": {
        "desc": "Each dictionary has the stat name as the key and the coordinates of the rectangle as the value.",
        "type_hint": "Dict[str, Any]",
        "Attack": ["The rectangle for Attack stat", (360, 220, 508, 308)],
        "Defense": ["The rectangle for Defense stat", (369, 396, 508, 472)],
        "Sp.Atk": ["The rectangle for Sp.Atk stat", (2, 218, 145, 319)],
        "Sp.Def": ["The rectangle for Sp.Def stat", (3, 396, 147, 487)],
        "Speed": ["The rectangle for Speed stat", (164, 463, 354, 526)],
    },
    "CROP_RECT_STAT_IV": {
        "desc": "Each dictionary has the stat name as the key and the coordinates of the rectangle as the value.",
        "type_hint": "Dict[str, Any]",
        "HP": ["The rectangle for HP IV Judge", (162, 191, 361, 218)],
        "Attack": ["The rectangle for Attack IV Judge", (366, 272, 508, 307)],
        "Defense": ["The rectangle for Defense IV Judge", (336, 440, 507, 474)],
        "Sp.Atk": ["The rectangle for Sp.Atk IV Judge", (3, 274, 147, 303)],
        "Sp.Def": ["The rectangle for Sp.Def IV Judge", (3, 442, 147, 471)],
        "Speed": ["The rectangle for Speed IV Judge", (159, 460, 347, 494)],
    },
    "CROP_RECT_MAIN_IMG_BASED": {
        "desc": "Each dictionary has the stat name as the key and the coordinates of the rectangle as the value.",
        "type_hint": "Dict[str, Any]",
        "Gender": ["The rectangle for the gender icon", (529, 68, 578, 106)],
    },
    "CROP_RECT_MAIN_TXT_BASED": {
        "desc": "Each dictionary has the stat name as the key and the coordinates of the rectangle as the value.",
        "type_hint": "Dict[str, Any]",
        "No.": ["The rectangle for the number of the Pokemon", (518, 178, 640, 209)],
        "Species": [
            "The rectangle for the species of the Pokemon",
            (646, 176, 790, 210),
        ],
        "Lv.": ["The rectangle for the level of the Pokemon", (651, 62, 784, 110)],
        "Move_1": [
            "The rectangle for the first move of the Pokemon",
            (603, 229, 797, 283),
        ],
        "Move_2": [
            "The rectangle for the second move of the Pokemon",
            (602, 288, 797, 339),
        ],
        "Move_3": [
            "The rectangle for the third move of the Pokemon",
            (604, 346, 798, 397),
        ],
        "Move_4": [
            "The rectangle for the fourth move of the Pokemon",
            (604, 404, 801, 459),
        ],
        "OT": [
            "The rectangle for the original trainer of the Pokemon",
            (625, 517, 842, 555),
        ],
        "TID": [
            "The rectangle for the trainer ID of the Pokemon",
            (996, 518, 1249, 554),
        ],
        "Nature": ["The rectangle for the nature of the Pokemon", (202, 562, 445, 596)],
        "Ability": [
            "The rectangle for the ability of the Pokemon",
            (204, 601, 447, 635),
        ],
        "Held Item": [
            "The rectangle for held item of the Pokemon",
            (201, 641, 444, 675),
        ],
        "Stat Judge": [
            "The rectangle for Stat Judge of the Pokemon",
            (43, 528, 470, 559),
        ],
    },
}

test_002_expected_output = {
    "CROP_RECT_FALSE": {
        "desc": "Constant for a false crop rectangle",
        "type_hint": "tuple",
        "val": "(0, 0, 0, 0)",
    },
    "SCALE_FACTOR": {
        "desc": "A constant for scaling",
        "type_hint": "float",
        "val": 2.0,
    },
    "MATCH_THRESHOLD": {
        "desc": "A constant for matching threshold",
        "type_hint": "float",
        "val": 0.8,
    },
    "GAUSSIAN_KERNEL_SIZE": {
        "desc": "A tuple for Gaussian kernel size",
        "type_hint": "Tuple[int, int]",
        "val": "(5, 5)",
    },
    "GAUSSIAN_SIGMA_X": {
        "desc": "A constant for Gaussian sigma X",
        "type_hint": "float",
        "val": 0.75,
    },
    "THRESHOLD_THRESH": {
        "desc": "A constant for thresholding threshold",
        "type_hint": "int",
        "val": 0,
    },
    "THRESHOLD_MAXVAL": {
        "desc": "A constant for thresholding max value",
        "type_hint": "int",
        "val": 255,
    },
    "NUMPY_ONES_SHAPES": {
        "desc": "A tuple for numpy ones shapes",
        "type_hint": "Tuple[int, int]",
        "val": "(1, 1)",
    },
    "DENOISE_FILTER_STRENGTH": {
        "desc": "A constant for denoising filter strength",
        "type_hint": "int",
        "val": 10,
    },
    "DENOISE_TEMPLATE_SIZE": {
        "desc": "A constant for denoising template size",
        "type_hint": "int",
        "val": 7,
    },
    "DENOISE_TEMPLATE_SEARCH": {
        "desc": "A constant for denoising template search",
        "type_hint": "int",
        "val": 21,
    },
    "NATURE_NEUTRAL": {
        "desc": "A constant for nature stats neutral",
        "type_hint": "str",
        "val": "Neutral",
    },
    "NATURE_MINUS": {
        "desc": "A constant for nature stats minus",
        "type_hint": "str",
        "val": "-",
    },
    "NATURE_PLUS": {
        "desc": "A constant for nature stats plus",
        "type_hint": "str",
        "val": "/+",
    },
    "GENDER_GENDERLESS": {
        "desc": "A constant for genderless gender of the Pokemon",
        "type_hint": "str",
        "val": "genderless",
    },
    "GENDER_MALE": {
        "desc": "A constant for male gender of the Pokemon",
        "type_hint": "str",
        "val": "male",
    },
    "GENDER_FEMALE": {
        "desc": "A constant for female gender of the Pokemon",
        "type_hint": "str",
        "val": "female",
    },
}
