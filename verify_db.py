import db_utils
from mysql.connector import Error
import os

print("Verifying database connection using .env credentials...")

# Debug config (masking password)
config = db_utils.DB_CONFIG.copy()
config['password'] = '******'
print(f"Loaded Config: {config}")

try:
    conn = db_utils.create_connection()
    if conn and conn.is_connected():
        print("\n[SUCCESS] Successfully connected to the database!")
        conn.close()
    else:
        print("\n[FAILURE] Connection returned None or is not connected.")
        # Try to print why
        if conn is None:
            print("Check db_utils.create_connection implementation.")
except Error as e:
    print(f"\n[FAILURE] Connection failed with MySQL Error: {e}")
except Exception as e:
    print(f"\n[FAILURE] An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
