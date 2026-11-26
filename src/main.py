import os
import polars as pl
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime


def create_table(pdf, df):
    with pdf.table(text_align=("LEFT", "RIGHT", "RIGHT")) as table:
        # Table Header
        header = table.row()
        for col in df.columns:
            header.cell(col)

        # Table Body
        for row in df.iter_rows():
            pdf_row = table.row()
            for value in row:
                pdf_row.cell(str(value))


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

# Create pdf page and put tables and chart in it
pdf = FPDF()
pdf.add_page()

# Create page title
pdf.set_font("Helvetica", size=18, style="B")

start_date = main_table["Date"].min()
end_date = main_table["Date"].max()

start = start_date.strftime("%d %b")
end = end_date.strftime("%d %b %Y")

title = f"Revenue Report from {start} to {end}"
pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")

# Create page subtitle
pdf.set_font("Helvetica", size=12)
creation_date = datetime.now().strftime("%d %b %Y")

subtitle = f"Created on {creation_date}"
pdf.cell(text=subtitle, new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

# Create Revenue by regions table with title
pdf.set_font(style="B")
pdf.cell(text="Regions Revenue", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font(style="")
create_table(pdf, regions_revenue)
pdf.ln(10)

# Create Revenue Chart with title
pdf.set_font(style="B")
pdf.cell(text="Revenue chart for the period", new_x="LMARGIN", new_y="NEXT")
file_path = f"{OUTPUT_PATH}/regions_revenue_chart.png"
pdf.image(file_path, w=150, h=100)
pdf.ln(10)

# Create Revenue by Products table with title
pdf.set_font(style="B")
pdf.cell(text="Products Revenue", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font(style="")
create_table(pdf, products_revenue)

pdf.output(f"{OUTPUT_PATH}/revenue_report.pdf")
