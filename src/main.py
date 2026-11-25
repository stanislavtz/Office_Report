import os
from tokenize import group

import polars as pl

# Read files and add them to one main table
files = os.listdir("../sales")

tables = []
for file in files:
    table = pl.read_excel(f"../sales/{file}")
    tables.append(table)

main_table = pl.concat(tables)

main_table = main_table.with_columns(Revenue=(main_table["Units"] * main_table["Unit Price"]))

regions_revenue = (main_table.select(["Region", "Units", "Revenue"])
                   .group_by("Region")
                   .agg(pl.col("Units", "Revenue").sum())
                   .sort("Revenue", descending=True))

products_revenue = (main_table.select(["Product", "Units", "Revenue"])
                    .group_by("Product")
                    .agg(pl.col("Units", "Revenue").sum())
                    .sort("Revenue", descending=True))

print(regions_revenue)
print(products_revenue)