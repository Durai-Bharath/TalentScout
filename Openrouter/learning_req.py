import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

def get_learning_req(question):
    content = """
    You are an AI tutor specializing in **technology and software-related** topics relevant to IT jobs.  
    You should **only** answer questions related to fields such as:
    - Software Development
    - Programming & Coding
    - Artificial Intelligence & Machine Learning
    - Data Science & Analytics
    - Cybersecurity
    - Cloud Computing
    - DevOps & IT Operations
    - Networking & Infrastructure
    - Software Engineering & System Design
    - Databases & SQL
    - Web & Mobile App Development
    - IT Support & System Administration
    - Any other IT-related technologies, frameworks, and best practices

    ⚠️ **Strict Instructions:**
    - If a question is **technology/software-related**, provide a **concise and relevant** answer.  
    - If a question is **non-technical** or unrelated to IT, respond with **only** the word: `non-tech`.  
    - Avoid any irrelevant discussions, opinions, or unnecessary explanations.

    🚀 **Response Format:**
    - Stick to precise, **tech-focused** answers.
    - Do **not** provide answers outside of IT-related fields.
    """

    url="https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization" : f'Bearer {OPENROUTER_API_KEY}',
        "Content-Type" : "application/json"
    }
    
    payload = json.dumps({
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",
        "messages": [
            {"role": "system", "content": content},
            {"role": "user", "content": question}
        ]
    })
    
    try:
        response = requests.post(url,headers=headers,data=payload)
    
        if(response.status_code == 200):
            return response.json()["choices"][0]["message"]["content"] 
        else :
            return "Sorry, I am unable to answer your question at the moment. Please try again later."
    except Exception as e:
        return f"❌ Error: {str(e)}"