import re
from schema import UnifiedDocument
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove noise tokens like [Music], [inaudible], [Laughter]
    noise_patterns = [
        r'\[Music\]',
        r'\[inaudible\]',
        r'\[Laughter\]',
        r'\[Applause\]',
        r'\[silence\]'
    ]
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Strip timestamps [00:00:00]
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)

    # Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    vietnamese_prices = {
        'không': 0, 'một': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5,
        'sáu': 6, 'bảy': 7, 'tám': 8, 'chín': 9, 'mười': 10,
        'trăm': 100, 'nghìn': 1000, 'triệu': 1000000
    }

    price_value = None
    for vn_phrase, value in vietnamese_prices.items():
        if vn_phrase in text.lower():
            price_value = value
            break

    doc = UnifiedDocument(
        document_id="transcript-001",
        content=text.strip(),
        source_type="Transcript",
        author="Unknown Speaker",
        timestamp=datetime.now(),
        source_metadata={
            'price_mentioned': price_value,
            'original_file': file_path
        }
    )

    return doc
