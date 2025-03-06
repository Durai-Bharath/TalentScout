import sqlite3 as sql
import json

def init_db():
    
    conn = sql.connect("talentScout.db")
    cursor = conn.cursor()

    drop_query = '''DROP TABLE IF EXISTS Job'''
    cursor.execute(drop_query)
    
    create_query_jobs = '''CREATE TABLE IF NOT EXISTS Job
    (job_id text PRIMARY KEY, job_name text, job_description text , skills text)'''

    cursor.execute(create_query_jobs)

    
    jobs = [
        {
            "job_id": "1",
            "job_name": "Software Engineer",
            "job_description": "Develop and maintain software applications.",
            "skills": ["Python", "Java", "SQL"]
        },
        {
            "job_id": "2",
            "job_name": "Machine Learning Engineer",
            "job_description": "Develop, deploy, and optimize ML models for real-world applications.",
            "skills": ["MLFlow", "Python", "TensorFlow", "SQL"]
        },
        {
            "job_id": "3",
            "job_name": "Data Analyst",
            "job_description": "Analyze and visualize data to drive business decisions.",
            "skills": ["Python", "Tableau", "SQL", "Excel"]
        },
        {
            "job_id": "4",
            "job_name": "Cybersecurity Engineer",
            "job_description": "Ensure system security by identifying and mitigating vulnerabilities.",
            "skills": ["Kali Linux", "Networking", "Python", "SIEM"]
        },
        {
            "job_id": "5",
            "job_name": "Cloud Engineer",
            "job_description": "Design and manage cloud infrastructure solutions.",
            "skills": ["AWS", "Azure", "Docker", "Kubernetes"]
        },
        {
            "job_id": "6",
            "job_name": "DevOps Engineer",
            "job_description": "Automate and improve the development and deployment pipelines.",
            "skills": ["Jenkins", "Docker", "Kubernetes", "Terraform"]
        },
        {
            "job_id": "7",
            "job_name": "Frontend Developer",
            "job_description": "Develop interactive and responsive UI components for web applications.",
            "skills": ["React", "JavaScript", "CSS", "TypeScript"]
        },
        {
            "job_id": "8",
            "job_name": "Backend Developer",
            "job_description": "Build and maintain server-side applications and databases.",
            "skills": ["Node.js", "Express", "MongoDB", "PostgreSQL"]
        },
        {
            "job_id": "9",
            "job_name": "AI Research Scientist",
            "job_description": "Conduct research and develop new AI/ML models for real-world problems.",
            "skills": ["Deep Learning", "PyTorch", "NLP", "Computer Vision"]
        },
        {
            "job_id": "10",
            "job_name": "Blockchain Developer",
            "job_description": "Develop and implement blockchain-based applications and smart contracts.",
            "skills": ["Solidity", "Ethereum", "Rust", "Cryptography"]
        }
    ]


    for job in jobs:
        job_id = job["job_id"]
        job_name = job["job_name"]
        job_description = job["job_description"]
        skills = job["skills"]
        cursor.execute("INSERT INTO Job VALUES(?,?,?,?)", (job_id, job_name, job_description, json.dumps(skills)))
    conn.commit()


    create_user_table = '''CREATE TABLE IF NOT EXISTS user
    (id text PRIMARY KEY, name text , email text , phone text , yoe real , location text ,
    job_id text, score real,
    FOREIGN KEY (job_id) REFERENCES Job(job_id))
    '''
    cursor.execute(create_user_table)


    conn.close()