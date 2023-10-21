import csv
from pathlib import Path
from typing import Any, Dict, List, TextIO, Tuple, Union

import yaml

# Define logging levels
LOGGING_LEVELS: List[int] = [50, 40, 30, 20, 10, 0]
LOG_LEVEL_KEYWORDS: List[str] = [
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
]


def getLoggingLevel(level_name: str) -> int:
    """
    Returns the logging level corresponding to the given level name.

    Parameters:
    level_name (str): The name of the logging level.

    Returns:
    int: The logging level.
    """
    return LOGGING_LEVELS[LOG_LEVEL_KEYWORDS.index(level_name)]


def generateConfig(cfg: dict) -> None:
    """
    Generates configuration files for each key in the given dictionary, excluding the 'version' key.

    Parameters:
    cfg (dict): The configuration dictionary.

    Returns:
    None
    """
    for key in cfg:
        if key != "version":
            with open(f"./generated/{key.upper()}.py", "w") as file:
                writeConfig(cfg, key, file)


def writeConfig(public_cfg: Dict[str, Any], cfg_name: str, stream: TextIO) -> None:
    """
    Writes the configuration to a file.

    Parameters:
    public_cfg (Dict[str, Any]): The public configuration dictionary.
    cfg_name (str): The name of the configuration.
    stream (TextIO): The file stream to write to.

    Returns:
    None
    """
    WRITE = stream.write
    WRITE(f'CONFIG_VERSION = "{public_cfg["version"]}"\n\n')

    for cfg in unnestDict(public_cfg[cfg_name]):
        left_side = "_".join([cfg_name.upper()] + [c.upper() for c in cfg[:-1]])
        right_side = cfg[-1]

        if isinstance(right_side, (int, float, bool, list)) or right_side == "None":
            WRITE(f"{left_side} = {right_side}\n")
        else:
            WRITE(f'{left_side} = "{right_side}"\n')


def unnestDict(
    nested_dict: Dict[str, Union[Dict, int, float, bool, list]], keys: List[str] = []
) -> List[Tuple]:
    """
    Unnests a dictionary.

    Parameters:
    nested_dict (dict): The dictionary to unnest.
    keys (list): The list of keys for the current level of nesting.

    Returns:
    list: A list of tuples, where each tuple contains the keys from the top level to the current level and the corresponding value.
    """
    result = []
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            result.extend(unnestDict(value, keys + [key]))
        else:
            result.append(tuple(keys + [key, value]))
    return result


def loadDTC() -> List[Dict[str, str]]:
    """
    Loads a CSV file and returns a list of dictionaries where each dictionary represents a row in the CSV.

    Returns:
    csv_db (List[Dict[str, str]]): A list of dictionaries where each dictionary represents a row in the CSV.
    """
    csv_db = []
    with open("./config/DTC.csv", mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_db.append(row)
    return csv_db


def generateDTC(csv_db: List[Dict[str, str]]) -> None:
    """
    Generates a Python file from a CSV database.

    Parameters:
    csv_db (List[Dict[str, str]]): The CSV database.

    Returns:
    None
    """
    with open("./generated/DTC.py", "w") as stream:
        WRITE = stream.write
        event_id_list = []
        current_event_status = 0
        for entry in csv_db:
            if not entry["EVENT ID"] in event_id_list:
                event_id_list.append(entry["EVENT ID"])
                current_event_status = 0
            else:
                current_event_status += 1
            DEM_EVENT = "{0}_{1}".format(entry["EVENT ID"], entry["EVENT STATUS"])
            WRITE(
                'DEM_EVENT_{0: <60}= ({2}, {3}, {4}, "{1}")\n'.format(
                    DEM_EVENT,
                    DEM_EVENT,
                    getLoggingLevel(entry["LOG LEVEL"]),
                    len(event_id_list),
                    current_event_status,
                )
            )


def loadConfig(file_path: str) -> Dict[str, Any]:
    """
    Loads a configuration file.

    Parameters:
    file_path (str): The path to the configuration file.

    Returns:
    cfg (Dict[str, Any]): The loaded configuration.
    """
    with open(file_path, "r") as stream:
        cfg = yaml.load(stream, Loader=yaml.CLoader)
    return cfg


def main() -> None:
    """
    Main function that generates configuration files and a Python file from a CSV database.

    Returns:
    None
    """
    Path("generated").mkdir(parents=True, exist_ok=True)

    public_cfg = loadConfig("./config/public_cfg.yml")
    # generateConfig(public_cfg)
    from src.pyPkmHome._generateCode import mainFunction
    mainFunction(public_cfg)

    # private_cfg = loadConfig("./config/private_cfg.yml")
    # generateConfig(private_cfg)

    # csv_db = loadDTC()
    # generateDTC(csv_db)


if __name__ == "__main__":
    # If this script is run as the main program, call the main function.
    main()

################################################################################
#                                END OF FILE                                   #
################################################################################
