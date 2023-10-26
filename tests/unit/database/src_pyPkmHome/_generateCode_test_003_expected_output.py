# This is a generated Python script
from typing import Any, Tuple, Dict
# Each dictionary has the stat name as the key and the coordinates of the rectangle as the value.
CROP_RECT_NATURE_STAT:  Dict[str, Any] = {
    # The rectangle for Attack stat
    "Attack": (360, 220, 508, 308),
    # The rectangle for Defense stat
    "Defense": (369, 396, 508, 472),
    # The rectangle for Sp.Atk stat
    "Sp.Atk": (2, 218, 145, 319),
    # The rectangle for Sp.Def stat
    "Sp.Def": (3, 396, 147, 487),
    # The rectangle for Speed stat
    "Speed": (164, 463, 354, 526),
}
# Each dictionary has the stat name as the key and the coordinates of the rectangle as the value.
CROP_RECT_STAT_IV:  Dict[str, Any] = {
    # The rectangle for HP IV Judge
    "HP": (162, 191, 361, 218),
    # The rectangle for Attack IV Judge
    "Attack": (366, 272, 508, 307),
    # The rectangle for Defense IV Judge
    "Defense": (336, 440, 507, 474),
    # The rectangle for Sp.Atk IV Judge
    "Sp.Atk": (3, 274, 147, 303),
    # The rectangle for Sp.Def IV Judge
    "Sp.Def": (3, 442, 147, 471),
    # The rectangle for Speed IV Judge
    "Speed": (159, 460, 347, 494),
}
# Each dictionary has the stat name as the key and the coordinates of the rectangle as the value.
CROP_RECT_MAIN_IMG_BASED:  Dict[str, Any] = {
    # The rectangle for the gender icon
    "Gender": (529, 68, 578, 106),
}
# Each dictionary has the stat name as the key and the coordinates of the rectangle as the value.
CROP_RECT_MAIN_TXT_BASED:  Dict[str, Any] = {
    # The rectangle for the number of the Pokemon
    "No.": (518, 178, 640, 209),
    # The rectangle for the species of the Pokemon
    "Species": (646, 176, 790, 210),
    # The rectangle for the level of the Pokemon
    "Lv.": (651, 62, 784, 110),
    # The rectangle for the first move of the Pokemon
    "Move_1": (603, 229, 797, 283),
    # The rectangle for the second move of the Pokemon
    "Move_2": (602, 288, 797, 339),
    # The rectangle for the third move of the Pokemon
    "Move_3": (604, 346, 798, 397),
    # The rectangle for the fourth move of the Pokemon
    "Move_4": (604, 404, 801, 459),
    # The rectangle for the original trainer of the Pokemon
    "OT": (625, 517, 842, 555),
    # The rectangle for the trainer ID of the Pokemon
    "TID": (996, 518, 1249, 554),
    # The rectangle for the nature of the Pokemon
    "Nature": (202, 562, 445, 596),
    # The rectangle for the ability of the Pokemon
    "Ability": (204, 601, 447, 635),
    # The rectangle for held item of the Pokemon
    "Held Item": (201, 641, 444, 675),
    # The rectangle for Stat Judge of the Pokemon
    "Stat Judge": (43, 528, 470, 559),
}
# Constant for a false crop rectangle
CROP_RECT_FALSE: tuple = (0, 0, 0, 0)
# A constant for scaling
SCALE_FACTOR: float = 2.0
# A constant for matching threshold
MATCH_THRESHOLD: float = 0.8
# A tuple for Gaussian kernel size
GAUSSIAN_KERNEL_SIZE: Tuple[int, int] = (5, 5)
# A constant for Gaussian sigma X
GAUSSIAN_SIGMA_X: float = 0.75
# A constant for thresholding threshold
THRESHOLD_THRESH: int = 0
# A constant for thresholding max value
THRESHOLD_MAXVAL: int = 255
# A tuple for numpy ones shapes
NUMPY_ONES_SHAPES: Tuple[int, int] = (1, 1)
# A constant for denoising filter strength
DENOISE_FILTER_STRENGTH: int = 10
# A constant for denoising template size
DENOISE_TEMPLATE_SIZE: int = 7
# A constant for denoising template search
DENOISE_TEMPLATE_SEARCH: int = 21
# A constant for nature stats neutral
NATURE_NEUTRAL: str = "Neutral"
# A constant for nature stats minus
NATURE_MINUS: str = "-"
# A constant for nature stats plus
NATURE_PLUS: str = "/+"
# A constant for genderless gender of the Pokemon
GENDER_GENDERLESS: str = "genderless"
# A constant for male gender of the Pokemon
GENDER_MALE: str = "male"
# A constant for female gender of the Pokemon
GENDER_FEMALE: str = "female"

################################################################################
#                                END OF FILE                                   #
################################################################################