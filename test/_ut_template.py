import functools
from unittest import IsolatedAsyncioTestCase
from collections.abc import Generator
from typing import Callable, Generator, Any, List
from inspect import iscoroutinefunction

import __params
import __expected


class clsUnitTestTemplate(IsolatedAsyncioTestCase):
    """A template for unit tests."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.checkpoint: List[Any] = list()
        self.check = self.checkpoint.append
        super().setUp()

    def tearDown(self) -> None:
        """Tear down the test case."""
        super().tearDown()

    def _get_input(self, test_case: str) -> Generator:
        """
        Get the input for a given test case.

        Args:
            test_case (str): The name of the test case.

        Returns:
            Generator: A generator that yields the inputs for the test case.
        """
        input = eval(f"__param.{test_case}")
        yield from input

    @staticmethod
    def _template_decorate(test_procedure: Callable):
        """
        Decorate the test procedure.

        Args:
            test_procedure (Callable): The test procedure to decorate.

        Returns:
            Callable: The decorated test procedure.
        """

        test_case = test_procedure.__name__[len("test_") :]
        if iscoroutinefunction(test_procedure):

            @functools.wraps(test_procedure)
            async def coroutine_wrapper(self) -> None:

                self.pre_test(test_case)
                await test_procedure(self)
                self.post_test(test_case)

            return coroutine_wrapper
        else:

            @functools.wraps(test_procedure)
            def wrapper(self) -> None:
                self.pre_test(test_case)
                test_procedure(self)
                self.post_test(test_case)

            return wrapper

    def pre_test(self, test_case: str):
        """
        Prepare for the test.

        Args:
            test_case (str): The name of the test case.
        """
        self.input = self._get_input(test_case).__next__

    def post_test(self, test_case: str):
        """
        Clean up after the test and check the results.

        Args:
            test_case (str): The name of the test case.
        """
        expected = eval(f"__expected.{test_case}")

        for i, result in enumerate(self.checkpoint):
            self.assertEqual(result, expected[i], f"Failed {test_case} point #{i+1}")

        self.checkpoint.clear()


################################################################################
#                                END OF FILE                                   #
################################################################################
