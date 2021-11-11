import sqlite3
from sqlite3 import Error
import time

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_task_id(conn, id):
    cur = conn.cursor()
    cur.execute(f"SELECT sequenza FROM Movimenti Where id = {id}")

    rows = cur.fetchall()

    for row in rows:
        print(row[0])

def main():
    conn = create_connection("./dbMovimenti")

    select_task_id(conn, input("Inserisci id: "))

if __name__ == "__main__":
    main()