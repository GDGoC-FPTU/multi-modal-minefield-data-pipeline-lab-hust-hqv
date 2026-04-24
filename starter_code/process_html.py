from bs4 import BeautifulSoup
from schema import UnifiedDocument
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    documents = []
    table = soup.find('table', {'id': 'main-catalog'})

    if not table:
        return documents

    rows = table.find_all('tr')[1:]  # Skip header row

    for idx, row in enumerate(rows):
        cols = row.find_all('td')
        if len(cols) < 3:
            continue

        product_name = cols[0].get_text(strip=True)
        price_text = cols[1].get_text(strip=True)
        description = cols[2].get_text(strip=True)

        # Handle N/A or Liên hệ in price column
        if price_text in ['N/A', 'Liên hệ', '']:
            price = None
        else:
            try:
                price = float(price_text.replace('$', '').replace(',', ''))
            except ValueError:
                price = None

        doc = UnifiedDocument(
            document_id=f"html-product-{idx}",
            content=f"Product: {product_name}\nDescription: {description}",
            source_type="HTML",
            author="Catalog System",
            timestamp=datetime.now(),
            source_metadata={
                'product_name': product_name,
                'price': price,
                'description': description
            }
        )
        documents.append(doc)

    return documents
