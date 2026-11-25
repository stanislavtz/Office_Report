## Project Overview

This project automates the generation and distribution of revenue reports.

### Workflow

1. Data is extracted from multiple **Excel (.xlsx)** files and consolidated into a single master dataset.
2. The master dataset is used to generate the following summary reports:
   - **Regional Report**: Aggregated revenue data grouped by region.
   - **Product Report**: Aggregated revenue data grouped by product.
3. A revenue chart is generated based on the Regional Report, visualizing the relationship between regions and revenue for a selected reporting period.
4. The generated reports and chart are compiled into a PDF document.
5. Once the PDF report is created, it is automatically sent via email to the director.

### Key Features

- Automated data consolidation from multiple Excel files
- Revenue analysis by region and product
- Automatic chart generation
- PDF report creation
- Automated email distribution
