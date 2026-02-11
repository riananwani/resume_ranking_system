import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('DB_HOST', 'localhost')
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', '')

print(f"Attempting connection to {host} as {user} with password length {len(password)}")

try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    if conn.is_connected():
        print("[SUCCESS] Connection established!")
        conn.close()
    else:
        print("[FAILURE] Connected but is_connected() returned False.")

except Error as e:
    print(f"[FAILURE] MySQL Error: {e}", flush=True)
except Exception as e:
    print(f"[FAILURE] General Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
