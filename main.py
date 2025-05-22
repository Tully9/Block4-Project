import psycopg2

conn = psycopg2.connect(
    host="ise-db.postgres.database.azure.com",
    port=5432,
    dbname="postgres",
    user="tom",
    password="Racing795!",
    sslmode="require"  # Disable server certificate verification
)

print("✅ Connected to Azure PostgreSQL!")
conn.close()

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "wassup beijing"

if __name__ == "__main__":
    # Make sure it's listening on 0.0.0.0 for external access
    app.run(host="0.0.0.0", port=80)
