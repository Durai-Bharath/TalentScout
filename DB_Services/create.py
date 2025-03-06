import sqlite3 as sql
import json

db_path = "talentScout.db"

def addUser(user):
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user VALUES(?,?,?,?,?,?,?,?)", (user["id"], user["name"], user["email"], user["phone"], user["yoe"], user["location"], user["job_id"], user["score"]))
    conn.commit()
    conn.close()
    print(f"Inserted {user['name']} into user table")   