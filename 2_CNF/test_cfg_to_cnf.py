import unittest
from cfg_to_cnf import CFGtoCNF

class TestCFGtoCNF(unittest.TestCase):
    def test_all_in_one(self):
        cfg = {
            'S': ['aSb', 'Z', '-'], # '-' represents Epsilon
            'Z': ['Y'],
            'Y': ['y'],
        }
        cnf = {
            'S': ['AB', 'AM0', 'y'],
            'M0': ['SB'],
            'Z': ['y'],
            'Y': ['y'],
            'A': ['a'],
            'B': ['b'],
        }
        obj = CFGtoCNF(cfg)
        self.assertEqual(obj.cfg_to_cnf(), cnf)

if __name__ == '__main__':
    unittest.main()