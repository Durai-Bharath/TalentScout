import streamlit as st
import sqlite3 as sql
from DB_Services.create import addUser
from DB_Services.read import getJobById
import uuid

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "job_id" not in st.session_state:
    st.session_state.job_id = None

def FormPage(job_id):

    if not job_id or job_id is None:
        st.error("No job selected! Please select a job first.")
        st.stop()
    
    st.session_state.job_id = job_id
    job_name = getJobById(job_id)[1]
    
    # CSS Styling
    st.markdown("""
        <style>
            .form-container {
                background-color: #ffffff;
                padding: 10px;
                border-radius: 15px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: auto;
                margin-bottom: 20px;
            }
            .form-header {
                font-size: 24px;
                font-weight: bold;
                color: #2b7bba;
                text-align: center;
            }
            .stButton > button {
                background-color: #2b7bba;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                width: 100%;
            }
            .job-title {
                font-size: 20px;
                font-weight: bold;
                color: #1a5a99;
                text-align: center;
                margin-bottom: 10px;
            }
            .stButton > button:hover {
                background-color: #1a5a99;
            }
        </style>
    """, unsafe_allow_html=True)

    # FORM CONTAINER
    with st.container():
        st.markdown(f'<div class="job-title">Apply for {job_name}</div>', unsafe_allow_html=True)
        st.markdown('<div class="form-container"><div class="form-header">Job Application Form 📝</div></div>', unsafe_allow_html=True)

        # Form starts here
        with st.form("job_application_form"):
            col1, col2 = st.columns(2)  # Split into two columns

            with col1:
                name = st.text_input("Full Name", max_chars=50)
                phone = st.text_input("Phone Number", max_chars=10)

            with col2:
                email = st.text_input("Email Address", max_chars=100)
                location = st.text_input("Location", max_chars=100)

            yoe = st.number_input("Years of Experience", min_value=1, max_value=50, step=1,value=1)

            submitted = st.form_submit_button("Submit Application")

        st.markdown('</div>', unsafe_allow_html=True)  # Close the form-container

    # Form Submission Logic
    if submitted:
        if not name or not email or not phone or not location:
            st.warning("Please fill in all required fields!")
        elif "@" not in email or "." not in email:
            st.warning("Please enter a valid email address!")
        elif not phone.isdigit() or len(phone) < 10:
            st.warning("Please enter a valid phone number!")
        else:
            user_id = str(uuid.uuid4())  # Generate unique user ID
            score = None  # Score will be updated later

            user  = {
                "id": user_id,
                "name": name,
                "email": email,
                "phone": phone,
                "yoe": yoe,
                'location': location,
                'job_id': job_id,
                'score': score
            }
            addUser(user)
            st.success("🎉 Application Submitted Successfully!")
            st.session_state.user_id = user_id  # Store user_id in session for chatbot
            st.session_state.job_id = job_id  # Ensure job_id is also stored in session
            st.rerun()  # Refresh the page to display the ChatBot