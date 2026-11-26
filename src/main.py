import os
import polars as pl
import matplotlib.pyplot as plt

OUTPUT_PATH = "../outputs"

# Read files and add them to one main table
files = os.listdir("../sales")
files = [f for f in files if  "~$" not in f]
files = [f for f in files if f.endswith(".xlsx")]

tables = []
for file in files:
    table = pl.read_excel(f"../sales/{file}")
    tables.append(table)

main_table = pl.concat(tables)

# Add additional column Revenue to the main table
main_table = main_table.with_columns(Revenue=(main_table["Units"] * main_table["Unit Price"]))

# Build Revenue table by Regions
regions_revenue = (main_table.select(["Region", "Units", "Revenue"])
                   .group_by("Region")
                   .agg(
                        pl.col("Units").sum(),
                        pl.col("Revenue").sum().cast(pl.Float64))
                   .sort("Revenue", descending=True))

# Build Revenue table by Products
products_revenue = (main_table.select(["Product", "Units", "Revenue"])
                    .group_by("Product")
                    .agg(
                        pl.col("Units").sum(),
                        pl.col("Revenue").sum().cast(pl.Float64))
                    .sort("Revenue", descending=True))

print(regions_revenue)
print(products_revenue)

# Implement bar chart based on the Regions and Revenues
regions = regions_revenue["Region"].to_list()
revenues = regions_revenue["Revenue"].to_list()

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(regions, revenues, color="#2F6690", width=0.6)

# Shows value label on top of the bars
ax.bar_label(bars, fmt="{:,.2f}", padding=3)

ax.set_title("Revenue by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Revenue")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))

# Quieter styling: no top/right frame, light horizontal grid behind the bars
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#DDDDDD", linewidth=0.8)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/regions_revenue_chart.png")
plt.show()
