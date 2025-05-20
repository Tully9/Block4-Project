import psycopg

# Connect to your database
conn = psycopg.connect(
    dbname="tomdb",
    user="postgres",
    password="test123",
    host="localhost",
    port="5432"
)

# Take input from the terminal
name = input("Enter the name of the user to update: ")
new_age = int(input(f"Enter the new age for {name}: "))

# Use parameterized SQL (to avoid SQL injection)
with conn.cursor() as cur:
    cur.execute(
        "UPDATE users SET age = %s WHERE name = %s",
        (new_age, name)
    )
    conn.commit()
    print(f"{cur.rowcount} row(s) updated.")

conn.close()
