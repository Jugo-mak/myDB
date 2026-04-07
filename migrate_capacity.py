import os
import psycopg2
from urllib.parse import urlparse

# Get connection string from database.py (we know it from viewing the file)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:agtj8512@localhost:5433/tents"
db_url = "postgresql://postgres:agtj8512@localhost:5433/tents"

print(f"Connecting to database to change capacity type...")
try:
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE tents ALTER COLUMN capacity TYPE numeric;")
    conn.commit()
    print("Successfully changed capacity column type to numeric.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error occurred: {e}")
