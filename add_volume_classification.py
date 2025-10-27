#!/usr/bin/env python3
"""
Script to add volume-based classification to search data CSV.
"""

import csv
from collections import Counter

def classify_volume(users):
    """
    Classify search volume based on number of users.

    Args:
        users: Number of users (string or int)

    Returns:
        str: Classification category
    """
    try:
        # Convert to int, handling potential string or empty values
        user_count = int(users)

        if user_count >= 1000:
            return "High Volume"
        elif user_count >= 500:
            return "Medium Volume"
        elif user_count >= 100:
            return "Niche Queries"
        elif user_count >= 10:
            return "Long tail Queries"
        else:
            return "Micro Tail Queries"
    except (ValueError, TypeError):
        return ""

def main():
    input_file = "BK Search Terms - Sheet1 (1).csv"
    output_file = "BK Search Terms - Sheet1 (1).csv"

    print(f"Reading {input_file}...")

    # Read the CSV file
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Add new column to header
        header.append('Volume based classification')
        rows.append(header)

        classifications = Counter()
        sample_rows = []

        for i, row in enumerate(reader):
            # Get users value (column index 1)
            if len(row) > 1:
                users = row[1]
                classification = classify_volume(users)
                row.append(classification)
                classifications[classification] += 1

                # Store first 20 rows for sample
                if i < 20:
                    sample_rows.append((row[0], users, classification))
            else:
                row.append('')

            rows.append(row)

    print(f"Total rows processed: {len(rows) - 1}")
    print(f"Columns: {header}")

    # Display sample of the classification
    print("\nSample classifications:")
    print(f"{'Query':<30} {'Users':<10} {'Classification'}")
    print("-" * 70)
    for query, users, classification in sample_rows:
        print(f"{query:<30} {users:<10} {classification}")

    # Show distribution of classifications
    print("\nClassification distribution:")
    for classification in sorted(classifications.keys()):
        print(f"  {classification}: {classifications[classification]}")

    # Save the modified CSV
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✓ Done! Volume classification column added successfully.")

if __name__ == "__main__":
    main()
