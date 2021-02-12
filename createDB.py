import sqlite3

connection = sqlite3.connect('test.db')

cursor = connection.cursor()

cursor.execute("""
      CREATE TABLE IF NOT EXISTS pw (
          siteName TEXT UNIQUE NOT NULL,
          pass TEXT NOT NULL
          )
    """)

connection.commit()
connection.close()