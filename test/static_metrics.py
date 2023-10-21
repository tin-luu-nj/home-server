import json
import os
import subprocess
from typing import List


def run_radon_commands(commands: List[str], save_output: bool = True) -> None:
    """
    Run radon commands on specified paths and optionally save the output to a file.

    Parameters:
    commands (List[str]): A list of radon commands to run.
    save_output (bool): If True, save the output to a file. Defaults to True.
    """
    radon_tool = "radon"
    code_paths = ["./src/", "./test/", "./Launcher.py"]
    report_directory = "./report/static"
    command_options = {
        "stdout": {
            "cc": ["-s", "--show-closures", "--total-average"],
            "raw": ["-s"],
            "mi": ["-s"],
            "hal": ["-f"],
        },
        "outfile": {"cc": ["-j"], "raw": ["-j"], "mi": ["-j"], "hal": ["-j"]},
    }

    for radon_command in commands:
        output_file_path = os.path.join(report_directory, f"{radon_command}.json")
        print(f"Running radon {radon_command}...")

        if save_output:
            with open(output_file_path, "w") as output_file:
                subprocess.run(
                    [radon_tool, radon_command]
                    + command_options["outfile"][radon_command]
                    + code_paths,
                    stdout=output_file,
                )

            print(
                f"Finished running radon {radon_command}. Output saved to {output_file_path}."
            )

            # Load JSON data from the file
            with open(output_file_path, "r") as output_file:
                json_data = json.load(output_file)

            # Pretty print JSON data to the same file
            with open(output_file_path, "w") as output_file:
                json.dump(json_data, output_file, indent=4)

        else:
            subprocess.run(
                [radon_tool, radon_command]
                + command_options["stdout"][radon_command]
                + code_paths
            )
            print(f"Finished running radon {radon_command}. Output not saved.")

        print(f"-------------------------------------------------------")


# Example usage
run_radon_commands(["cc", "raw", "mi", "hal"], save_output=True)
