import psycopg

# Connect to your PostgreSQL database
conn = psycopg.connect(
    dbname="tomdb",
    user="postgres",
    password="test123",
    host="localhost",
    port="5432"
)

# Take user input
name = input("Enter user's name: ")
email = input("Enter user's email: ")
age = int(input("Enter user's age: "))

# Insert the new user into the table
with conn.cursor() as cur:
    cur.execute(
        "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
        (name, email, age)
    )
    conn.commit()
    print(f"User '{name}' added successfully.")

conn.close()
