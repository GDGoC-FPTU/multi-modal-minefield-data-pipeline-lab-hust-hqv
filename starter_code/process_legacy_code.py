import ast
from schema import UnifiedDocument
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    tree = ast.parse(source_code)

    docstrings = []
    business_rules = []

    # Use the 'ast' module to find docstrings for functions
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings.append(f"{node.name}: {docstring}")

    # Use regex to find business rules in comments like "# Business Logic Rule 001"
    for line in source_code.split('\n'):
        if '# Business Logic Rule' in line or '# Rule' in line:
            business_rules.append(line.strip())

    content = "\n".join(docstrings + business_rules)

    doc = UnifiedDocument(
        document_id="code-001",
        content=content if content else "No docstrings or business rules found",
        source_type="Code",
        author="Legacy System",
        timestamp=datetime.now(),
        source_metadata={
            'docstrings_count': len(docstrings),
            'business_rules_count': len(business_rules),
            'original_file': file_path
        }
    )

    return doc
