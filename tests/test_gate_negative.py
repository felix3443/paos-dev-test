import unittest


class GateNegative(unittest.TestCase):
    def test_red_on_purpose(self):
        self.fail("deliberately red to test the merge gate")
