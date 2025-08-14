import unittest
from generate_large_csv import generate_csv

class TestGenerateLargeCSV(unittest.TestCase):
    def test_generate_csv_creates_file(self):
        import os
        test_filename = "test_output.csv"
        generate_csv(test_filename, diff_row=10, diff_col=2)
        self.assertTrue(os.path.exists(test_filename))
        # Optionally, check header and row count
        with open(test_filename) as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 1_000_001)  # header + 1,000,000 rows
        os.remove(test_filename)

if __name__ == "__main__":
    unittest.main()
