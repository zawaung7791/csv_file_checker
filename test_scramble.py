import unittest
from pathlib import Path
import polars as pl
import os
from scramble import scramble

class TestScramble(unittest.TestCase):
    def setUp(self):
        # Create a small CSV for testing
        self.input_csv = Path("test_input.csv")
        self.output_csv = Path("test_scrambled.csv")
        with open(self.input_csv, "w") as f:
            f.write("a,b,c\n1,2,3\n4,5,6\n7,8,9\n")

    def tearDown(self):
        if self.input_csv.exists():
            os.remove(self.input_csv)
        if self.output_csv.exists():
            os.remove(self.output_csv)

    def test_scramble_creates_output(self):
        scramble(self.input_csv, self.output_csv, show=False)
        self.assertTrue(self.output_csv.exists())
        df = pl.read_csv(str(self.output_csv))
        self.assertEqual(df.shape[0], 3)
        self.assertEqual(set(df.columns), {"a", "b", "c"})

if __name__ == "__main__":
    unittest.main()
