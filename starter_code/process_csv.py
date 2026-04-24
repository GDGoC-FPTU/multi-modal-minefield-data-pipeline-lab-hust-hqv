import pandas as pd
from schema import UnifiedDocument
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    df = pd.read_csv(file_path)

    # Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')

    # Clean 'price' column: convert "$1200", "250000", "five dollars" to floats
    def clean_price(price_str):
        if pd.isna(price_str):
            return None
        price_str = str(price_str).strip()
        price_str = price_str.replace('$', '').replace(',', '')

        # Handle text numbers like "five dollars"
        text_numbers = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'hundred': 100, 'thousand': 1000, 'million': 1000000
        }

        words = price_str.lower().split()
        if all(w in text_numbers for w in words):
            result = 0
            for word in words:
                result += text_numbers[word]
            return float(result)

        try:
            return float(price_str)
        except ValueError:
            return None

    df['price'] = df['price'].apply(clean_price)

    # Normalize 'date_of_sale' into a single format (YYYY-MM-DD)
    def normalize_date(date_str):
        if pd.isna(date_str):
            return None
        try:
            parsed = pd.to_datetime(date_str)
            return parsed.strftime('%Y-%m-%d')
        except:
            return None

    df['date_of_sale'] = df['date_of_sale'].apply(normalize_date)

    # Return a list of dictionaries for the UnifiedDocument schema
    documents = []
    for idx, row in df.iterrows():
        doc = UnifiedDocument(
            document_id=f"csv-{row['id']}",
            content=f"Sales Record: ID={row['id']}, Price={row['price']}, Date={row['date_of_sale']}",
            source_type="CSV",
            author="Sales System",
            timestamp=datetime.fromisoformat(row['date_of_sale']) if row['date_of_sale'] else None,
            source_metadata={
                'id': row['id'],
                'price': row['price'],
                'date_of_sale': row['date_of_sale']
            }
        )
        documents.append(doc)

    return documents

