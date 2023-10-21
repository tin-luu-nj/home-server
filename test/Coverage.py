import os
import sys

# get the current working directory
# add the current working directory to sys.path
sys.path.append(os.getcwd())
os.environ['COVERAGE_RCFILE'] = 'test/.coveragerc'

import unittest

import coverage
from html_reporter import HTMLTestRunner


def run_tests_with_coverage() -> None:
    """
    Run unit tests with coverage.

    Args:
        test_files (List[str]): List of test files to be run.

    Returns:
        None
    """
    # Start the coverage collection
    cov = coverage.Coverage()
    cov.start()

    runner = HTMLTestRunner(
        report_filepath="report/ut/UnitTest.html",
        verbosity=2,
        title="Unit Test Report",
        open_in_browser=True,
    )

    # Your test suite here
    combined_suite = unittest.TestSuite()
    suite = unittest.defaultTestLoader.discover(
        start_dir="./test/unittest/", pattern="*_test.py"
    )
    combined_suite.addTest(suite)

    runner.run(combined_suite)

    # Stop and save the coverage data
    cov.stop()
    cov.save()

    # Generate the report
    with open("./report/cov_ut/cov_ut.md", "w") as stream:
        cov.report(output_format="markdown", file=stream)
    cov.html_report(directory="./report/cov_ut/html/")


# Call the function with the list of test files
run_tests_with_coverage()
