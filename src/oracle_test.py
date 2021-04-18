import os
import cx_Oracle


USERNAME = os.environ.get('ORACLE_USERNAME')
PASSWORD = os.environ.get('ORACLE_PASSWORD')
SERVER = os.environ.get('ORACLE_SERVER')
DATABASE = os.environ.get('ORACLE_DATABASE')

print("ORACLE_HOME:", os.environ.get('ORACLE_HOME'))
print("Parameters:", f"User: {USERNAME}, Pass: {PASSWORD}, Host: {SERVER}, Database: {DATABASE}")

connection = cx_Oracle.connect(USERNAME, PASSWORD, f"{SERVER}/{DATABASE}", encoding="UTF-8")

print(connection.version)
connection.close()