import os, sys
sys.path.append(os.getcwd()) if os.getcwd() not in sys.path else None
os.environ['COVERAGE_RCFILE'] = 'tests/.coveragerc'

import pytest

def run_tests_with_coverage():
    """
    Run unit tests with coverage using pytest.

    Returns:
        None
    """
    # Define the command with necessary options for pytest and pytest-cov
    command = [
        '-vv',  # increase verbosity
        '--cov-report=html:./report/cov_ut/html/',  # generate HTML report
        '--cov-report=term',  # display coverage on the terminal
        '--cov=.',  # specify which package to cover
        './tests/unit/'  # specify where the test scripts are
    ]

    # Run pytest with the defined command
    pytest.main(command)

# Call the function to run the tests with coverage
run_tests_with_coverage()
