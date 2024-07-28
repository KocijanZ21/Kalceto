import os

# Specify the path to the file
file_path = 'C:/Users/Uporabnik/Desktop/Baze_projekt/Kalceto/Data/models.py'

# Check if the file exists
if os.path.isfile(file_path):
    print(f"{file_path} exists.")
else:
    print(f"{file_path} does not exist.")

# Data/repository.py

import sys
import os
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Print current working directory
print("Current working directory:", os.getcwd())

# Ensure the parent directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Print sys.path for debugging
print("sys.path:", sys.path)

try:
    from Data import auth_public as auth  # Absolute import
    print("Import successful.")
except ImportError as e:
    print("ImportError:", e)

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

