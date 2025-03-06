import streamlit as st
import sqlite3 as sql
from Stages.form import FormPage
from Stages.bot import ChatBot
from Stages.botLearning import learningChat
from Stages.botInterview import botInterview
from Stages.leaderBoard import leaderboard
from DB_Services.read import getJobOpening
import json
from DB_Init.db_init import init_db


if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True
    
# Initialize session state for job selection and user
if "job_id" not in st.session_state:
    st.session_state.job_id = None
    
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "learning_chat" not in st.session_state:
    st.session_state.learning_chat = False
    
if "chat_started" not in st.session_state :
    st.session_state.chat_started = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "response" not in st.session_state:
    st.session_state.response = None

if "loading" not in st.session_state:
    st.session_state.loading = False 


    
if "skills" not in st.session_state:
    st.session_state.skills = []
    st.session_state.current_skill_index = 0
    st.session_state.difficulty = {}
    st.session_state.score = {}
    st.session_state.wrong_attempts = {}
    st.session_state.prev_answers = {}
    st.session_state.current_question = None
    st.session_state.questions_asked = {}
    st.session_state.final_score = 0
    st.session_state.chat_history = []
    st.session_state.isInterviewStarted = False
    st.session_state.clear_input = False


if st.session_state.job_id is not None and st.session_state.user_id is None:
    FormPage(st.session_state.job_id)
    
if st.session_state.user_id is not None and st.session_state.job_id is not None and st.session_state.chat_started == False and st.session_state.learning_chat == False:
    ChatBot(st.session_state.job_id, st.session_state.user_id) 


if st.session_state.learning_chat:
    learningChat()


if st.session_state.chat_started:
    botInterview()
    

#Home Page  
def Home():
    # Streamlit Page Configuration
    # st.set_page_config(page_title="Talent Scout", page_icon="✌️", layout="wide")

    st.title("Welcome to Talent Scout 🚀")
    st.header("We have the following job openings:")

 
    
    jobs = getJobOpening()

    # Apply styling using CSS
    st.markdown("""
        <style>
            .job-card {
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 10px;
                width: 100%;
                display: flex;
                margin-top: 30px;
                flex-direction: column;
            }
            .job-title {
                font-size: 22px;
                font-weight: bold;
                color: #2b7bba;
                margin-bottom: 10px;
            }
            .job-description {
                font-size: 16px;
                color: #333;
                margin-bottom: 10px;
            }
            .skills {
                font-size: 14px;
                color: #555;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)


    # Display jobs in a properly styled card format
    for job in jobs:
        job_id, job_name, job_description, skills = job 
        skills_list = ", ".join(json.loads(skills))  # Convert skills from JSON to string

        # Using HTML to maintain structure
        job_card = f"""
        <div class="job-card">
            <div class="job-title">{job_name}</div>
            <div class="job-description">{job_description}</div>
            <div class="skills"><b>Skills Required:</b> {skills_list}</div>
        </div>
        """
        
        # Display the job card
        st.markdown(job_card, unsafe_allow_html=True)

        # Apply button to apply for the job
        if st.button(f"Apply for {job_name}", key=f"job_{job_id}"):
            st.session_state.job_id = job_id
            st.rerun()

    st.markdown("---")  # Add a separator for better UI
    leaderboard()
    st.markdown("---")  # Add a separator for better UI
if st.session_state.job_id is None:
    Home()
    

