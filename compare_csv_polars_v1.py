import time
import polars as pl

start_time = time.time()

def read_csv(filepath):
    return pl.read_csv(filepath)

def compare_csv(file1, file2):

    # Read full CSVs, using inferred dtypes where possible
    df1 = pl.read_csv(file1, infer_schema_length=None)
    df2 = pl.read_csv(file2, infer_schema_length=None)

    # Sort both dataframes by all columns to ensure consistent row order
    df1 = df1.sort(df1.columns)
    df2 = df2.sort(df2.columns)

    results = {
        "shape_match": False,
        "number_of_columns_match": False,
        "column_names_match": False,
        "column_types_match": False,
        "data_match": False
    }

    # compare the shape
    if df1.shape == df2.shape:
        results["shape_match"] = True

    # compare number of columns
    if len(df1.columns) == len(df2.columns):
        results["number_of_columns_match"] = True

    # compare number and names of columns
    if list(df1.columns) == list(df2.columns):
        results["column_names_match"] = True

    # check the datatypes of each column
    types_match = True
    for col in df1.columns:
        if col in df2.columns:
            dtype1 = df1.schema[col]
            dtype2 = df2.schema[col]
            if dtype1 != dtype2:
                types_match = False
    results["column_types_match"] = types_match

    # compare data
    data_match = True
    if df1.shape == df2.shape and list(df1.columns) == list(df2.columns):
        if not df1.equals(df2, null_equal=True):
            data_match = False
        else:
            data_match = True
    else:
        data_match = False
    results["data_match"] = data_match

    # Print conclusion
    print("\n--- Comparison Summary ---")
    print(f"File 1 shape: {df1.shape}, File 2 shape: {df2.shape}")
    print(f"Number of columns - File 1: {len(df1.columns)}, File 2: {len(df2.columns)}")
    print(f"Number of matching column names: {len(set(df1.columns) & set(df2.columns))} / {max(len(df1.columns), len(df2.columns))}")
    print(f"Column datatypes match: {results['column_types_match']}")
    print(f"Data matches: {results['data_match']}")

    # print the mismatched columns and datatypes
    if not results["column_types_match"]:
        print("\n--- Mismatched Columns and Datatypes ---")
        for col in df1.columns:
            if col in df2.columns:
                dtype1 = df1.schema[col]
                dtype2 = df2.schema[col]
                if dtype1 != dtype2:
                    print(f"Column '{col}': {dtype1} != {dtype2}")

    # Output mismatched rows with row_number, payer, payer_description, and mismatched columns as separate columns
    if not results["data_match"]:
        print("\n--- Mismatched Rows ---")
        mismatched_rows = []
        for idx in range(df1.height):
            mismatched_cols = []
            mismatched_values = {}
            for col in df1.columns:
                val1 = df1[col][idx]
                val2 = df2[col][idx]
                if val1 is None and val2 is None:
                    continue
                if val1 != val2:
                    mismatched_cols.append(col)
                    mismatched_values[col] = f"{val1} != {val2}"
            if mismatched_cols:
                row_info = {
                    "row_number": idx + 1,
                    "payer": df1["C-Customer_Payer"][idx] if "C-Customer_Payer" in df1.columns else None,
                    "payer_description": df1["C-Name"][idx] if "C-Name" in df1.columns else None,
                    "material": df1["M-Material"][idx] if "M-Material" in df1.columns else None,
                    "material description": df1["M-Description"][idx] if "M-Description" in df1.columns else None
                }
                # Add each mismatched column as a separate column
                for col in mismatched_cols:
                    row_info[col] = mismatched_values[col]
                mismatched_rows.append(row_info)
        if mismatched_rows:
            mismatch_df = pl.DataFrame(mismatched_rows)
            print(mismatch_df)
        else:
            print("No mismatched rows found.")
    
    print(f"--- Elapsed Time ---")
    print(f"{time.time() - start_time:.2f} seconds")

    return results

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Compare two CSV files.')
    parser.add_argument('file1', type=str, help='Path to the first CSV file')
    parser.add_argument('file2', type=str, help='Path to the second CSV file')

    args = parser.parse_args()
    compare_csv(args.file1, args.file2)

