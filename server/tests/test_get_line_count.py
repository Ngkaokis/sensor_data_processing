import os
import unittest

from server.worker.utils import get_line_count

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "data/data_1.csv")


class GetLineCountTest(unittest.TestCase):
    def test_get_line_count(self):
        count = get_line_count(TESTDATA_FILENAME)
        self.assertEqual(count, 10)
