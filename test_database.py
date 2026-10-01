from database import engine

try:
    connection = engine.connect()
    print("Database connection successful!")
    connection.close()

except Exception as error:
    print("Database connection failed!")
    print(error)