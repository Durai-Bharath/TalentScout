import sqlite3 as sql
import json

db_path = r"DB_Init\talentScout.db"

def getJobById(job_id):
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Job WHERE job_id=?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job


def getUserById(user_id):
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def getJobOpening():
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Job")
    jobs = cursor.fetchall()
    conn.close()
    return jobs



def getSkillsByJobId(job_id):
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT skills FROM Job WHERE job_id=?", (job_id,))
    skills = cursor.fetchone()
    conn.close()
    return json.loads(skills[0]) if skills else []

def getAllUsers():
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT u.name,u.email,u.phone,u.yoe,u.location,j.job_name,u.score FROM user u JOIN Job j ON u.job_id = j.job_id where u.score > 0 ORDER BY u.score DESC") 
    users = cursor.fetchall()
    conn.close()
    return users