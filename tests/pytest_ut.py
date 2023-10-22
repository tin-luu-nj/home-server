import pytest

def run_tests():
    command = [
        "-vv",
        "-rP",
        "--html=report/ut/report.html",
        "./tests/unit/",
    ]
    # Specify the test file or directory and the HTML report file as strings in the list
    pytest.main(command)

run_tests()
