from database import get_db_connection


try:
    connection = get_db_connection()
    print("✅ Database connection successful!")

    cursor = connection.cursor()
    cursor.execute("SELECT version();")

    result = cursor.fetchone()
    print("PostgreSQL:", result[0])

    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Database connection failed!")
    print("Error:", e)