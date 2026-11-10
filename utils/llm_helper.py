import ollama


def generate_database_design(business_description, model="phi3"):

    prompt = f"""
You are a database architect.

Design a relational database schema for the following business idea:

{business_description}

Return EXACTLY 3 sections.

SECTION 1: DATABASE DESIGN
List tables with columns, primary keys, and foreign keys.

SECTION 2: SQL CREATE TABLE
Write valid SQL CREATE TABLE statements.

SECTION 3: ER DIAGRAM
Describe relationships using format:
TableA --(1:N)--> TableB

Rules:
- Every table must have a primary key
- Foreign keys must reference primary keys
- Use junction tables for many-to-many relationships
- Do not include explanations inside SQL
"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]