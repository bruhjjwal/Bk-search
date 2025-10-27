#!/usr/bin/env python3
"""
Script to add intent-based classification to search data CSV.
"""

import csv
import re
from collections import Counter

# Define keyword sets for classification
PRODUCTS = {
    't shirt', 'tshirt', 't-shirt', 'shirt', 'shirts', 'joggers', 'jeans', 'vest', 'vests',
    'hoodie', 'hoodies', 'hoddie', 'hoddies', 'shoes', 'shoe', 'shorts', 'bag', 'bags',
    'cargo', 'cargos', 'lower', 'lowers', 'jacket', 'jackets', 'cap', 'caps', 'pants',
    'pant', 'sneakers', 'sneaker', 'tops', 'top', 'dress', 'dresses', 'skirt', 'skirts',
    'sweater', 'sweaters', 'sweatshirt', 'sweatshirts', 'trackpant', 'trackpants',
    'trousers', 'trouser', 'kurta', 'kurtas', 'boxers', 'boxer', 'briefs', 'socks',
    'sandals', 'sandal', 'slippers', 'slipper', 'slides', 'sliders', 'boots', 'boot',
    'backpack', 'backpacks', 'bagpack', 'bagpacks', 'wallet', 'wallets', 'belt', 'belts',
    'watch', 'watches', 'sunglasses', 'scarf', 'scarves', 'gloves', 'tie', 'ties', 'bow',
    'suit', 'suits', 'blazer', 'blazers', 'coat', 'coats', 'pyjama', 'pyjamas', 'pajama',
    'pajamas', 'nightwear', 'innerwear', 'underwear', 'bra', 'bras', 'panty', 'panties',
    'leggings', 'jeggings', 'shrug', 'shrugs', 'cardigan', 'cardigans', 'pullover',
    'pullovers', 'sweatpants', 'polo', 'polos', 'tank', 'tanks', 'camisole', 'camisoles',
    'blouse', 'blouses', 'saree', 'sarees', 'salwar', 'kurti', 'kurtis', 'dupatta',
    'dupattas', 'jersey', 'jerseys', 'sando', 'chinos', 'crocs', 'phone cover',
    'phone case', 'phonecover', 'phonecase'
}

GENDER_TERMS = {
    'for men', 'for women', 'men', 'women', "men's", "women's", 'mens', 'womens',
    'male', 'female', 'boys', 'girls', 'boy', 'girl', 'kids', 'unisex'
}

COLORS = {
    'white', 'black', 'red', 'blue', 'green', 'yellow', 'pink', 'purple', 'orange',
    'brown', 'grey', 'gray', 'navy', 'maroon', 'beige', 'olive', 'khaki', 'cream',
    'golden', 'silver', 'multicolor', 'multicolour', 'navy blue', 'light blue',
    'dark blue', 'sky blue', 'royal blue', 'lime green', 'dark green'
}

STYLES = {
    'printed', 'oversized', 'baggy', 'slim', 'slim fit', 'skinny', 'straight',
    'regular', 'fit', 'loose', 'tight', 'stretch', 'ripped', 'distressed',
    'acid wash', 'acidwash', 'graphic', 'plain', 'solid', 'striped', 'checkered',
    'checked', 'half sleeve', 'full sleeve', 'sleeveless', 'long sleeve',
    'short sleeve', 'crop', 'cropped', 'high waist', 'low waist', 'v neck',
    'v-neck', 'round neck', 'collar', 'hooded', 'zip', 'button', 'pocket',
    'embroidered', 'vintage', 'retro', 'classic', 'premium', 'basic', 'essential',
    'combo', 'set', 'pack', 'fitted', 'relaxed', 'tapered', 'bootcut', 'flared',
    'wide leg', 'denim', 'cotton', 'polyester', 'leather', 'wool', 'linen',
    'silk', 'nylon', 'lycra', 'spandex', 'fleece', 'velvet', 'satin', 'chiffon',
    'glow in dark', 'glow in the dark', 'glow', 'fluorescent', 'neon', 'reflective'
}

CHARACTERS_THEMES = {
    'anime', 'batman', 'marvel', 'naruto', 'superman', 'one piece', 'harry potter',
    'spiderman', 'venom', 'deadpool', 'goku', 'iron man', 'loki', 'friends',
    'game of thrones', 'squid game', 'nasa', 'panda', 'f1', 'formula 1', 'dragon ball',
    'pokemon', 'pikachu', 'avengers', 'captain america', 'thor', 'hulk', 'flash',
    'joker', 'harley quinn', 'wonder woman', 'aquaman', 'star wars', 'mandalorian',
    'baby yoda', 'mickey mouse', 'disney', 'marvel', 'dc', 'demon slayer', 'tanjiro',
    'nezuko', 'attack on titan', 'bleach', 'tokyo ghoul', 'jujutsu kaisen', 'my hero academia',
    'one punch man', 'death note', 'hunter x hunter', 'fairy tail', 'breaking bad',
    'money heist', 'stranger things', 'the office', 'rick and morty', 'peaky blinders',
    'game of thrones', 'got', 'friends', 'office', 'breaking bad', 'bb', 'loki',
    'wanda', 'vision', 'wandavision', 'falcon', 'winter soldier', 'black panther',
    'doctor strange', 'ant man', 'guardians', 'groot', 'rocket', 'thanos', 'infinity',
    'coffee', 'tiger', 'lion', 'skull', 'rose', 'flower', 'music', 'guitar', 'motorcycle',
    'bike', 'car', 'dog', 'cat', 'wolf', 'eagle', 'dragon', 'phoenix', 'tribal',
    'geometric', 'abstract', 'minimalist', 'mandala', 'galaxy', 'space', 'nature'
}

OCCASIONS = {
    'gym', 'formal', 'sports', 'workout', 'office', 'casual', 'party', 'wedding',
    'festive', 'beach', 'travel', 'running', 'yoga', 'fitness', 'athleisure',
    'loungewear', 'nightwear', 'sleepwear', 'activewear', 'sportswear', 'workwear',
    'partywear', 'party wear', 'ethnic', 'traditional', 'western', 'indo western'
}

def normalize_query(query):
    """Normalize query for better matching."""
    return query.lower().strip()

def contains_product(query):
    """Check if query contains any product keyword."""
    query_lower = normalize_query(query)
    for product in PRODUCTS:
        # Use word boundary matching to avoid partial matches
        if re.search(r'\b' + re.escape(product) + r'\b', query_lower):
            return True
    return False

def contains_gender(query):
    """Check if query contains gender terms."""
    query_lower = normalize_query(query)
    for gender in GENDER_TERMS:
        if gender in query_lower:
            return True
    return False

def contains_color(query):
    """Check if query contains color terms."""
    query_lower = normalize_query(query)
    for color in COLORS:
        if re.search(r'\b' + re.escape(color) + r'\b', query_lower):
            return True
    return False

def contains_style(query):
    """Check if query contains style terms."""
    query_lower = normalize_query(query)
    for style in STYLES:
        if re.search(r'\b' + re.escape(style) + r'\b', query_lower):
            return True
    return False

def contains_character(query):
    """Check if query contains character/theme terms."""
    query_lower = normalize_query(query)
    for character in CHARACTERS_THEMES:
        if re.search(r'\b' + re.escape(character) + r'\b', query_lower):
            return True
    return False

def contains_occasion(query):
    """Check if query contains occasion terms."""
    query_lower = normalize_query(query)
    for occasion in OCCASIONS:
        if re.search(r'\b' + re.escape(occasion) + r'\b', query_lower):
            return True
    return False

def count_modifiers(query):
    """Count how many modifier types are present."""
    count = 0
    if contains_gender(query):
        count += 1
    if contains_color(query):
        count += 1
    if contains_style(query):
        count += 1
    return count

def classify_intent(query):
    """
    Classify search intent based on query structure.

    Returns:
        str: Intent classification
    """
    if not query or not query.strip():
        return ""

    has_product = contains_product(query)
    has_character = contains_character(query)
    has_occasion = contains_occasion(query)
    has_gender = contains_gender(query)
    has_color = contains_color(query)
    has_style = contains_style(query)

    # CATEGORY C: OCCASION/LIFESTYLE INTENT
    if has_occasion:
        if has_product:
            return "C.2 Product + Occasion"
        else:
            return "C.1 Bare Occasion"

    # CATEGORY B: DISCOVERY INTENT (Character/Theme)
    if has_character:
        if has_gender and has_product:
            return "B.3 Character + Gender + Product"
        elif has_product:
            return "B.2 Product + Character"
        elif has_gender:
            return "B.3 Character + Gender"
        else:
            return "B.1 Bare Character/Theme"

    # CATEGORY A: NAVIGATIONAL INTENT (Product-focused)
    if has_product:
        modifier_count = count_modifiers(query)

        # A.5 Product + Multiple Modifiers (2 or more modifiers)
        if modifier_count >= 2:
            return "A.5 Product + Multiple Modifiers"

        # A.4 Product + Style (style but no gender/color, or style with only one other modifier)
        if has_style and not (has_gender and has_color):
            if has_gender or has_color:
                return "A.5 Product + Multiple Modifiers"
            return "A.4 Product + Style"

        # A.3 Product + Color (color but no gender/style)
        if has_color and not has_gender and not has_style:
            return "A.3 Product + Color"

        # A.2 Product + Gender (gender but no color/style)
        if has_gender and not has_color and not has_style:
            return "A.2 Product + Gender"

        # A.1 Bare Product (product only, no modifiers)
        if not has_gender and not has_color and not has_style:
            return "A.1 Bare Product"

        # Default to multiple modifiers if we have product + any combination we didn't catch
        return "A.5 Product + Multiple Modifiers"

    # If nothing matches, return uncategorized
    return "Uncategorized"

def main():
    input_file = "BK Search Terms - Sheet1 (1).csv"
    output_file = "BK Search Terms - Sheet1 (1).csv"

    print(f"Reading {input_file}...")

    # Read the CSV file
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Check if the column already exists
        intent_col_exists = 'Intent based classification' in header
        if intent_col_exists:
            intent_col_index = header.index('Intent based classification')
            print(f"Found existing 'Intent based classification' column at index {intent_col_index}. Will update it.")
        else:
            # Add new column to header
            header.append('Intent based classification')
            intent_col_index = len(header) - 1
            print(f"Adding new 'Intent based classification' column at index {intent_col_index}.")

        rows.append(header)

        classifications = Counter()
        sample_by_category = {}

        for i, row in enumerate(reader):
            # Get query value (column index 0)
            if len(row) > 0:
                query = row[0]
                classification = classify_intent(query)

                # Update or append the classification
                if intent_col_exists:
                    # Replace existing value
                    if len(row) > intent_col_index:
                        row[intent_col_index] = classification
                    else:
                        # Extend row if needed
                        while len(row) <= intent_col_index:
                            row.append('')
                        row[intent_col_index] = classification
                else:
                    # Append new value
                    row.append(classification)

                classifications[classification] += 1

                # Store samples for each category (first 3 examples)
                if classification not in sample_by_category:
                    sample_by_category[classification] = []
                if len(sample_by_category[classification]) < 3:
                    users = row[1] if len(row) > 1 else "N/A"
                    sample_by_category[classification].append((query, users))
            else:
                if not intent_col_exists:
                    row.append('')

            rows.append(row)

    print(f"Total rows processed: {len(rows) - 1}")
    print(f"Columns: {header}")

    # Show distribution of classifications
    print("\n" + "="*80)
    print("INTENT-BASED CLASSIFICATION DISTRIBUTION")
    print("="*80)

    # Group by main category
    category_a = {k: v for k, v in classifications.items() if k.startswith('A.')}
    category_b = {k: v for k, v in classifications.items() if k.startswith('B.')}
    category_c = {k: v for k, v in classifications.items() if k.startswith('C.')}
    other = {k: v for k, v in classifications.items() if not k[0] in ['A', 'B', 'C']}

    if category_a:
        print("\nCATEGORY A: NAVIGATIONAL INTENT")
        print("-" * 80)
        for classification in sorted(category_a.keys()):
            count = category_a[classification]
            print(f"\n{classification}: {count} queries")
            if classification in sample_by_category:
                print("  Examples:")
                for query, users in sample_by_category[classification]:
                    print(f"    - {query} ({users} users)")

    if category_b:
        print("\n\nCATEGORY B: DISCOVERY INTENT")
        print("-" * 80)
        for classification in sorted(category_b.keys()):
            count = category_b[classification]
            print(f"\n{classification}: {count} queries")
            if classification in sample_by_category:
                print("  Examples:")
                for query, users in sample_by_category[classification]:
                    print(f"    - {query} ({users} users)")

    if category_c:
        print("\n\nCATEGORY C: OCCASION/LIFESTYLE INTENT")
        print("-" * 80)
        for classification in sorted(category_c.keys()):
            count = category_c[classification]
            print(f"\n{classification}: {count} queries")
            if classification in sample_by_category:
                print("  Examples:")
                for query, users in sample_by_category[classification]:
                    print(f"    - {query} ({users} users)")

    if other:
        print("\n\nOTHER")
        print("-" * 80)
        for classification in sorted(other.keys()):
            count = other[classification]
            print(f"\n{classification}: {count} queries")
            if classification in sample_by_category and len(sample_by_category[classification]) > 0:
                print("  Examples:")
                for query, users in sample_by_category[classification][:5]:
                    print(f"    - {query} ({users} users)")

    # Save the modified CSV
    print(f"\n\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✓ Done! Intent classification column added successfully.")

if __name__ == "__main__":
    main()
