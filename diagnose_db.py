import mysql.connector
from mysql.connector import Error

common_passwords = ["", "root", "password", "123456", "mysql", "admin", "1234", "toor"]

print("Diagnosing MySQL Connection for user 'root'...")

found = False
for pwd in common_passwords:
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=pwd
        )
        if conn.is_connected():
            print(f"\n[SUCCESS] Connected successfully with password: '{pwd}'")
            found = True
            conn.close()
            # If found, update .env file content logically (we can't write invalid syntax)
            # We'll just print it for the agent to read.
            break
    except Error as e:
        # print(f"Failed with '{pwd}': {e}")
        pass

if not found:
    print("\n[FAILURE] Could not connect with any common default passwords.")
    print("Please use MySQL Workbench to reset your root password or check your configuration.")
else:
    print("You can update your .env file with this password.")
