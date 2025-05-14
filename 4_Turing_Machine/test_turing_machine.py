import unittest
from turing_machine import TuringMachine

class TestTuringMachine(unittest.TestCase):
    # All functions must start with prefix `test_`
    def test_normal_input(self):
        tm = TuringMachine('1011')
        self.assertEqual(tm.run(), '1100') # 1011 + 1 = 1100
    
    def test_all_ones(self):
        tm = TuringMachine('111')
        self.assertEqual(tm.run(), '1000') 
    
    def test_single_zero(self):
        tm = TuringMachine('0')
        self.assertEqual(tm.run(), '1')

    def test_empty_tape(self): 
        tm = TuringMachine('')
        self.assertEqual(tm.run(), '1') # Treat as single zero 
    
    def test_leading_zeros(self):
        tm = TuringMachine('0010')
        self.assertEqual(tm.run(), '0011') # Ignore leading zeros

if __name__ == '__main__':
    unittest.main()  