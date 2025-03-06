import streamlit as st
import json
from DB_Services.read import getJobById, getUserById

def ChatBot(job_id, user_id):
    # Retrieve user and job details
    job = getJobById(job_id)
    user = getUserById(user_id)

    if not job or not user:
        st.error("Invalid job or user details. Please try again.")
        return
    
    job_name = job[1]
    job_description = job[2]
    job_skills = ", ".join(json.loads(job[3]))  # Assuming skills are stored as a list
    username = user[1]

    # Initialize session state for chatbot
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    if "learning_chat" not in st.session_state:
        st.session_state.learning_chat = False

    # Header Section
    st.title("TalentScout - AI Interview Bot 🤖")
    
    # Job & User Details Section
    with st.expander(f"📌 Applying for: {job_name}", expanded=True):
        st.write(f"**Description:** {job_description}")
        st.write(f"**Required Skills:** {job_skills}")

    # Chatbot Initial Message
    st.markdown(f"""
    <div style="background:#f0f2f6;padding:15px;border-radius:10px;margin-top:10px;">
        <b>🤖 AI Bot:</b> Hey <b>{username}</b>, welcome to <b>TalentScout</b>! 🚀  
        I'm here to guide you through an <b>AI-driven interview</b> for the <b>{job_name}</b> role.  
        <br>
        🔍 I'll ask you questions based on the required skills and evaluate your responses.  
        🏆 At the end, you'll receive a <b>final score</b> based on your answers!  
        <br><br>
        🎯 Ready to showcase your skills?
        <br>  
        ✅ Tap <b>Start Interview</b> to begin the evaluation.  
        <br>
        📚 Tap <b>Start Learning</b> to explore key concepts before the interview.  
    </div>
    """, unsafe_allow_html=True)


    # # Buttons for User Interaction
    # col1, col2 = st.columns([1, 1])
    # with col1:
    col = st.columns([1])[0]
    with col:
        st.write(" ")
        
    if st.button("💫 Start Interview"):
        st.session_state.chat_started = True
        st.rerun()
        
    # with col2:
    if st.button("🏫 Start Learning"):
        st.session_state.learning_chat = True
        st.rerun()

    # # Start Chatbot when clicked
    # if st.session_state.chat_started:
    #     st.markdown("### 📝 Interview in Progress...")
    #     # Add your chat logic here
    #     st.write("🔹 Question 1: Describe your experience with [skill]?")
    #     st.text_input("Your Answer:")
