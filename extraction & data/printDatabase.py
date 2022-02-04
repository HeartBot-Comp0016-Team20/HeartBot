import sqlite3

if __name__=="__main__":
    conn = sqlite3.connect('data.db')
    cursor = conn.execute("SELECT * FROM tablename2")
    for row in cursor:
        print(row)
    conn.commit()
    conn.close()