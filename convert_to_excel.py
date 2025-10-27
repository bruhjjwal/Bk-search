#!/usr/bin/env python3
"""
Script to convert CSV to Excel format (.xlsx)
"""

import csv

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    USE_OPENPYXL = True
except ImportError:
    USE_OPENPYXL = False
    print("openpyxl not available, trying alternative method...")

def convert_with_openpyxl():
    """Convert CSV to Excel using openpyxl."""
    input_file = "BK Search Terms - Sheet1 (1).csv"
    output_file = "BK Search Terms - Sheet1.xlsx"

    print(f"Reading {input_file}...")

    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Search Data"

    # Read CSV and write to Excel
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row_idx, row in enumerate(reader, start=1):
            for col_idx, value in enumerate(row, start=1):
                ws.cell(row=row_idx, column=col_idx, value=value)

            if row_idx % 5000 == 0:
                print(f"  Processed {row_idx} rows...")

        print(f"  Total rows: {row_idx}")

    # Style the header row
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font

    # Auto-adjust column widths for first few columns
    for col_idx in range(1, 6):
        ws.column_dimensions[chr(64 + col_idx)].width = 20

    # Save the workbook
    print(f"\nSaving to {output_file}...")
    wb.save(output_file)
    print(f"✓ Successfully converted to Excel format!")
    print(f"  File: {output_file}")

    return output_file

def convert_with_csv_library():
    """Fallback: Create a simpler conversion."""
    try:
        import xlsxwriter

        input_file = "BK Search Terms - Sheet1 (1).csv"
        output_file = "BK Search Terms - Sheet1.xlsx"

        print(f"Reading {input_file}...")

        # Create workbook
        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet('Search Data')

        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#366092',
            'font_color': 'white'
        })

        # Read CSV and write to Excel
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for row_idx, row in enumerate(reader):
                for col_idx, value in enumerate(row):
                    if row_idx == 0:
                        worksheet.write(row_idx, col_idx, value, header_format)
                    else:
                        worksheet.write(row_idx, col_idx, value)

                if row_idx % 5000 == 0:
                    print(f"  Processed {row_idx} rows...")

        print(f"  Total rows: {row_idx + 1}")
        workbook.close()

        print(f"\n✓ Successfully converted to Excel format!")
        print(f"  File: {output_file}")

        return output_file

    except ImportError:
        print("ERROR: No Excel library available (openpyxl or xlsxwriter)")
        print("Please install one: pip install openpyxl")
        return None

if __name__ == "__main__":
    if USE_OPENPYXL:
        output_file = convert_with_openpyxl()
    else:
        output_file = convert_with_csv_library()

    if output_file:
        print(f"\nYou can now open '{output_file}' in Excel without any warnings!")
