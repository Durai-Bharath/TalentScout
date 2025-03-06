from sentence_transformers import SentenceTransformer, util
import requests
import os
from dotenv import load_dotenv
import json
import torch

torch.classes.__path__ = []

load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')


def getRelevantAnswer(prompt):
    url="https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization" : f'Bearer {OPENROUTER_API_KEY}',
        "Content-Type" : "application/json"
    }
    
    payload = json.dumps({
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",
        "messages": [
            {"role": "system", "content": prompt}
        ]
    })
    
    try:
        response = requests.post(url,headers=headers,data=payload)
        if(response.status_code == 200):
            return response.json()["choices"][0]["message"]["content"] 
        else :
            return "error"
        
    except Exception as e:
        return f"error"

def generateQuestions(skill,difficulty,prev_answer):
    prompt = f"""
    You are an AI interviewer conducting a technical screening.
    Your task is to generate a **{difficulty}**-level **theoretical** question for the skill: **{skill}**.

    ⚠️ **Rules:**
    - Do **NOT** repeat any of these previous questions: {prev_answer}.
    - Provide **only the question**, nothing else.
    - Keep it **clear, concise, and relevant** to {skill}.
    - Focus strictly on **theoretical knowledge**, avoiding implementation-based or coding-related questions.

    💡 **Thinking Process (Sometimes include this in output):**
    <think>
    - Consider the core theoretical concepts of {skill}.
    - Ensure the question tests understanding rather than application.
    - Formulate a question that assesses foundational principles, definitions, or conceptual explanations.
    </think>

    🚀 **Output Format:**
    - Occasionally, include the `<think>` section before the question.
    - Otherwise, just output the question.
    """


    url="https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization" : f'Bearer {OPENROUTER_API_KEY}',
        "Content-Type" : "application/json"
    }
    
    payload = json.dumps({
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",
        "messages": [
            {"role": "system", "content": prompt}
        ]
    })
    
    try:
        response = requests.post(url,headers=headers,data=payload)
        if(response.status_code == 200):
            if(response.json()["choices"][0]["message"]["content"] == ""):
                return generateQuestions(skill,difficulty,prev_answer)
            return response.json()["choices"][0]["message"]["content"] 
        else :
            return "Sorry, I am unable to generate a question at the moment. Please try again later."
        
    except Exception as e:
        return f"❌ Error: {str(e)}"
    
    

def evaluate_answer(user_answer, expected_answer):
    # Load sentence transformer model for similarity scoring
    model = SentenceTransformer("all-MiniLM-L6-v2")
    user_embedding = model.encode(user_answer, convert_to_tensor=True)
    expected_embedding = model.encode(expected_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(user_embedding, expected_embedding).item()
    return round(similarity * 10)    
