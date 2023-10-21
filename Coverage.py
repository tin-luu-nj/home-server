import coverage
import unittest
from html_reporter import HTMLTestRunner

# Start the coverage collection
cov = coverage.Coverage()
cov.start()

# Your test suite here
suite = unittest.defaultTestLoader.discover(start_dir='./test/', pattern='Diagnostic_ut.py')
runner = HTMLTestRunner(
        report_filepath="my_report.html",
        title="My unit test",
        description="This demonstrates the report output by HTMLTestRunner.",
        open_in_browser=True
    )
# runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)

# Stop and save the coverage data
cov.stop()
cov.save()

# Generate the report
cov.report()
cov.html_report()
