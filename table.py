import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    Id INTEGER PRIMARY KEY,
                    Title TEXT NOT NULL,
                    Desc TEXT NOT NULL,
                    Date TEXT NOT NULL,
                    Priority TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Call create_table function before running the Flask app
create_table()
