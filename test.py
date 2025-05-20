import psycopg

psycopg.connect(
    dbname="tomdb",
    user="postgres",
    password="test123",
    host="localhost",
    port="5432"
)

CompanyPositions = {
    # Company : Interview positions
    "Stripe" : 6,
    "AWS" : 18,
    "J&J" : 6,
    "CloudCards" : 6,
    "Dogpatch labs" : 6,
    "Patch" : 6,
    "Fidelity" : 6,
    "Transact Campus" : 3
}

StudentList = ["24412155", "24486331", "24810385", "24123443", "24900042", "24154365", "24777666", "24555555"]
