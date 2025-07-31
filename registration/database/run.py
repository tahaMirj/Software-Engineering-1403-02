import mysql.connector
from query import create_db_connection, describe_table
from english_website.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

table_name = 'Reading_Passages'

describe = describe_table(mydb, table_name)

if describe:
    print(f"Table structure for '{table_name}':")
    for column in describe:
        print(column)
else:
    print("Failed to retrieve table structure.")