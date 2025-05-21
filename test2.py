import psycopg
from psycopg.rows import dict_row

# Connect to the database
conn = psycopg.connect("dbname=tomdb user=postgres password=test123")
cur = conn.cursor(row_factory=dict_row)

# Fetch all table names in the 'public' schema
cur.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
""")
tables = cur.fetchall()

# Loop through each table and print contents
for row in tables:
    table_name = row['table_name']
    print(f"\n📦 Table: {table_name}")
    
    cur.execute(f"SELECT * FROM {table_name}")
    records = cur.fetchall()

    if not records:
        print("  (empty)")
    else:
        for record in records:
            print(f"  {record}")

# Clean up
cur.close()
conn.close()
