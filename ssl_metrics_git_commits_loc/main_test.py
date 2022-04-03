from dateutil.parser import parse as dateParse
from argparse import Namespace
import unittest
import main

class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_repoExists(self) -> None:
        trueDirectory: str = "../"
        falseDirectory: str = "./"
        self.assertTrue(main.repoExists(directory=trueDirectory))
        self.assertFalse(main.repoExists(directory=falseDirectory))
        self.assertTrue(type(main.repoExists(directory=trueDirectory)) == bool)
        self.assertTrue(type(main.repoExists(directory=falseDirectory)) == bool)

    def test_parseCommitLineFromLog(self)   ->  None:
        name: str = "Wild E. Coyote"
        email: str = "wec@mail.com"
        hash: str = "123abc"
        date: str = "1-2-90"    # Month - Day - Year
        parameter: str = ";".join([name, email, hash, date])
        testCase: dict = {"author_name": name, "author_email": email, "hash": hash, "date": dateParse(date)}
        self.assertTrue(main.parseCommitLineFromLog(line=parameter) == testCase)
