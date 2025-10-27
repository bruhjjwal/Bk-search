#!/usr/bin/env python3
"""
Script to remove duplicate 'Intent based classification' column.
"""

import csv

input_file = "BK Search Terms - Sheet1 (1).csv"
output_file = "BK Search Terms - Sheet1 (1).csv"

print(f"Reading {input_file}...")

rows = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    print(f"Original header has {len(header)} columns")
    print(f"Header: {header}")

    # Find all occurrences of 'Intent based classification'
    intent_indices = [i for i, col in enumerate(header) if col == 'Intent based classification']
    print(f"\nFound 'Intent based classification' at indices: {intent_indices}")

    if len(intent_indices) > 1:
        # Keep only the first occurrence, remove others
        indices_to_remove = set(intent_indices[1:])
        print(f"Will remove columns at indices: {indices_to_remove}")

        # Filter header
        header = [col for i, col in enumerate(header) if i not in indices_to_remove]
        rows.append(header)

        # Filter all rows
        for row in reader:
            filtered_row = [val for i, val in enumerate(row) if i not in indices_to_remove]
            rows.append(filtered_row)
    else:
        print("No duplicate columns found.")
        rows.append(header)
        for row in reader:
            rows.append(row)

print(f"\nNew header has {len(header)} columns")
print(f"Total rows: {len(rows)}")

# Save the fixed CSV
print(f"\nSaving to {output_file}...")
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("✓ Done! Duplicate column removed.")
