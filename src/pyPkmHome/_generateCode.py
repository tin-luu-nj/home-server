from typing import Any, Dict, List

from jinja2 import Template


def createRetangleDict(raw: Dict[str, Any], filter: List) -> Dict[str, Any]:
    """
    Extracts a nested dictionary from the raw data and reformats it.

    Parameters:
    raw (Dict[str, Any]): The raw data containing the nested dictionary.

    Returns:
    Dict[str, str]: A new dictionary with the extracted and reformatted data.
    """
    result = {}
    for stat_type in filter:
        stat_dict = raw["pokemon_HOME"]["crop_rectangle"][stat_type]
        for key, value in stat_dict.items():
            if key == "var":
                result[value] = {}
                current = result[value]
            elif key in ["desc", "type_hint"]:
                current[key] = value
            else:
                current[value["stat"]] = [
                    value["desc"],
                    (value["x1"], value["y1"], value["x2"], value["y2"]),
                ]
    return result


def extractDict(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts a nested dictionary from the raw data and reformats it.

    Parameters:
    raw (Dict[str, Any]): The raw data containing the nested dictionary.

    Returns:
    Dict[str, Any]: A new dictionary with the extracted and reformatted data.
    """
    # Extract the const dictionary
    const = raw["pokemon_HOME"]["const"]

    # Create the new dictionary
    result = {}
    for key, value in const.items():
        if not key == "desc":
            result[value["var"]] = {
                "desc": value["desc"],
                "type_hint": value["type_hint"],
                "val": value["value"],
            }
    return result


def mainFunction(raw: Dict[str, Any]) -> None:
    """
    This function takes a dictionary of raw data, applies it to a template,
    and writes the rendered output to a .py file.

    Args:
        raw (Dict[str, Any]): The raw data to be applied to the template.
    """
    with open("src/pyPkmHome/_CONST_template.txt") as file_:
        template = Template(file_.read())
        
    # Define data for the template
    data = {
        "crop_rect": createRetangleDict(
            raw, ["nature_stat", "stat_iv", "main_img_based", "main_txt_based"]
        ),
        "const": extractDict(raw),
    }

    # Render the template with the data
    output = template.render(data)
    print(output)

    # Write the output to a .py file
    with open("src/pyPkmHome/_CONST_.py", "w") as f:
        f.write(output)


################################################################################
#                                END OF FILE                                   #
################################################################################
