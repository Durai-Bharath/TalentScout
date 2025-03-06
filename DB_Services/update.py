import sqlite3 as sql
import json

db_path = r"DB_Init\talentScout.db"

def updateScore(user_id,score):
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET score = ? WHERE id = ?", (score, user_id))
    conn.commit()
    conn.close()
   
