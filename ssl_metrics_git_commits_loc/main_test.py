from argparse import Namespace
import unittest
import main

class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_repoExists(self) -> bool:
        trueDirectory: str = "../"
        falseDirectory: str = "./"
        self.assertTrue(main.repoExists(directory=trueDirectory))
        self.assertFalse(main.repoExists(directory=falseDirectory))
        self.assertTrue(type(main.repoExists(directory=trueDirectory)) == bool)
        self.assertTrue(type(main.repoExists(directory=falseDirectory)) == bool)
