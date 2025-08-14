# This script generates two large CSV files with 40 columns and 1,000,000 rows each for testing purposes.
import csv
import random

num_rows = 1_000_000
num_cols = 40

header = [f"col_{i+1}" for i in range(num_cols)]

# Generate first file
def generate_csv(filename, diff_row=None, diff_col=None):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row_idx in range(num_rows):
            row = [random.randint(0, 1000000) for _ in range(num_cols)]
            # Introduce a difference if specified
            if diff_row is not None and row_idx == diff_row:
                row[diff_col] += 1
            writer.writerow(row)

generate_csv("test1.csv")
