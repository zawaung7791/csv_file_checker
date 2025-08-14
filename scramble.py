import polars as pl

load_df = pl.read_parquet("..\\..\\pricing-exploratory-data-analysis\\data\\2022_2024_copa_product_customer.parquet")

scrambled_df = load_df.sample(n=load_df.height, with_replacement=False)
scrambled_df.write_parquet("..\\..\\pricing-exploratory-data-analysis\\data\\scrambled_2022_2024_copa_product_customer.parquet")