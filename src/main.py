import os
import polars as pl

# Read files and add them to one main table
files = os.listdir("../sales")

tables = []
for file in files:
    table = pl.read_excel(f"../sales/{file}")
    tables.append(table)

main_table = pl.concat(tables)

print(main_table)