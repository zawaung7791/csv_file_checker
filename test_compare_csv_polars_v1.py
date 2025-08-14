import unittest
import polars as pl
import os
from compare_csv_polars_v1 import compare_csv

class TestCompareCSV(unittest.TestCase):
    def setUp(self):
        # Create two CSVs with 1000 rows and 10 columns for testing
        self.file1 = "test_file1.csv"
        self.file2 = "test_file2.csv"
        data = {f"col_{i}": list(range(1, 1001)) for i in range(10)}
        df1 = pl.DataFrame(data)
        df2 = pl.DataFrame(data)
        df1.write_csv(self.file1)
        df2.write_csv(self.file2)

    def tearDown(self):
        if os.path.exists(self.file1):
            os.remove(self.file1)
        if os.path.exists(self.file2):
            os.remove(self.file2)

    def test_compare_identical(self):
        results = compare_csv(self.file1, self.file2)
        self.assertTrue(results["shape_match"])
        self.assertTrue(results["number_of_columns_match"])
        self.assertTrue(results["column_names_match"])
        self.assertTrue(results["column_types_match"])
        self.assertTrue(results["data_match"])

    def test_compare_different_data(self):
        # Change one value in file2 (row 500, col_5)
        df2 = pl.read_csv(self.file2)
        values = df2["col_5"].to_list()
        values[499] += 1000  # row 500 (0-based index)
        df2 = df2.with_columns([
            pl.Series("col_5", values)
        ])
        df2.write_csv(self.file2)
        results = compare_csv(self.file1, self.file2)
        self.assertFalse(results["data_match"])

if __name__ == "__main__":
    unittest.main()
