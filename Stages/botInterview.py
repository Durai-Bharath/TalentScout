import streamlit as st
import json
from DB_Services.read import getSkillsByJobId
from DB_Services.update import updateScore
from Openrouter.interview_req import generateQuestions, getRelevantAnswer, evaluate_answer

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
    st.session_state.isAnalyzing = False  # New flag for analyzing status
    st.session_state.isFetchingQuestion = False  # New flag for analyzing status
    st.session_state.user_answer = ""
    st.session_state.learning_chat = False
    st.session_state.clear_input = False

    
def botInterview():
    st.title("🎯 AI-Powered Screening Chatbot")
    st.write("🤖 I'm here to evaluate your skills for the job role.")
    skills = getSkillsByJobId(st.session_state.job_id)
    if not st.session_state.isInterviewStarted:
        if st.button("🚀 Start Screening") and skills :
            st.session_state.isInterviewStarted = True
            st.session_state.skills = skills
            for skill in skills:
                st.session_state.difficulty[skill] = "easy"
                st.session_state.score[skill] = 0
                st.session_state.wrong_attempts[skill] = 0
                st.session_state.prev_answers[skill] = []
                st.session_state.questions_asked[skill] = 0
            
            st.session_state.current_skill_index = 0    
            st.session_state.isFetchingQuestion = True
            if st.session_state.isFetchingQuestion:
                st.info("🔍 Fetching your first question...")
            current_question = generateQuestions(skills[0], "easy", [])
            st.session_state.isFetchingQuestion = False  
            st.session_state.current_question = current_question
            st.session_state.chat_history = []
            st.rerun()
            
    else:
        if st.button("❌ Exit Screening"):
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
            st.session_state.isAnalyzing = False 
            st.session_state.learning_chat = False  
            st.session_state.chat_started = False      
            st.rerun()
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(message["content"], unsafe_allow_html=True)
            else:
                st.write(message["content"])
    if st.session_state.clear_input:
        st.session_state.clear_input = False
        st.session_state.user_answer = ""

    if "current_question" in st.session_state and st.session_state.current_question:
        if st.session_state.current_skill_index >= len(st.session_state.skills):
            st.success("Screening Completed!")
            st.session_state.final_score = sum(st.session_state.score.values()) / (len(st.session_state.skills) * 50) * 100
            updateScore(st.session_state.user_id,st.session_state.final_score)
            if st.session_state.final_score >= 80:
                st.success("Final Verdict: Strong Fit ✅")
            elif st.session_state.final_score >= 50:
                st.warning("Final Verdict: Moderate Fit ⚠️")
            else:
                st.error("Final Verdict: Not a Fit ❌")
            verdict_message = "🎉 Congratulations! You have successfully completed the screening process." if st.session_state.final_score >= 80 else "🔍 You may need to improve your skills to be a strong fit for this role."
            # 🔹 Display popup with percentage score
            st.toast(f"🎯 Your final score: {st.session_state.final_score:.2f}%\n{verdict_message}", icon="🔥")

            if st.button("Restart Interview"):
                st.session_state.clear()
                st.rerun()
        else:
            skill = st.session_state.skills[st.session_state.current_skill_index]
            
            st.subheader(f"Skill: {skill} ({st.session_state.questions_asked[skill] + 1}/5)")
            progress = (st.session_state.questions_asked[skill]) / 5
            st.progress(progress)
        
            with st.chat_message("assistant"):
                st.write(f"Question: {st.session_state['current_question']}")
            
            user_answer = st.text_area("Your Answer:",key="user_answer")

            if st.button("Submit Answer") and user_answer:
                st.session_state.isAnalyzing = True
                
                
                if st.session_state.isAnalyzing:
                    st.info("🔍 Analyzing your answer...")
                
                expected_answer_prompt = f"Please Provide an ideal answer for this question: {st.session_state['current_question']}"
                expected_response = getRelevantAnswer(expected_answer_prompt)
                st.session_state.isAnalyzing = False
                if expected_response == "error":
                    with st.chat_message("assistant"):
                        st.error("❌ Error: Something went wrong. Please try again later.")
                        st.stop()
                else:
                    expected_answer = expected_response
                
                score = evaluate_answer(user_answer, expected_answer)
                st.session_state.score[skill] += score
                st.session_state.prev_answers[skill].append(st.session_state['current_question'])
                st.session_state.questions_asked[skill] += 1
                st.session_state.chat_history.append({"role": "user", "content": user_answer})
        
                # st.session_state.user_answer =  user_answer
                if score >= 7:
                    score_display = f"""
                    <div style="background-color:#D4EDDA; padding:6px; border-radius:10px; color:#155724; font-weight:bold;">
                    ✅ Great Job! Score: <span style='font-size:20px;'>{score}/10</span>
                    </div>
                    """
                elif 4 <= score < 7:
                    score_display = f"""
                    <div style="background-color:#FFF3CD; padding:6px; border-radius:10px; color:#856404; font-weight:bold;">
                    ⚠️ Decent! Score: <span style='font-size:20px;'>{score}/10</span>
                    </div>
                    """
                else:
                    score_display = f"""
                    <div style="background-color:#F8D7DA; padding:6px; border-radius:10px; color:#721C24; font-weight:bold;">
                    ❌ Needs Improvement. Score: <span style='font-size:20px;'>{score}/10</span>
                    </div>
                    """
                st.session_state.chat_history.append({"role": "assistant", "content": score_display})
                st.session_state.clear_input = True
                
                if score >= 6:
                    st.session_state.difficulty[skill] = "medium" if st.session_state.difficulty[skill] == "easy" else "hard"
                    st.session_state.wrong_attempts[skill] = 0
                    if st.session_state.questions_asked[skill] >= 5:
                        st.session_state.current_skill_index += 1
                else:
                    st.session_state.wrong_attempts[skill] += 1
                    if st.session_state.wrong_attempts[skill] >= 2 or st.session_state.questions_asked[skill] >= 5:
                        st.warning(f"Screening Stopped for {skill}: Performance is below the required level.")
                        st.session_state.current_skill_index += 1
                                
                if st.session_state.current_skill_index < len(st.session_state.skills):
                    next_skill = st.session_state.skills[st.session_state.current_skill_index]
                    st.session_state.current_question = generateQuestions(next_skill, st.session_state.difficulty[next_skill], st.session_state.prev_answers[next_skill])
                else:
                    st.success("Screening Completed!")
                
                st.rerun()
         
    # else:
    #     if st.session_state.current_question == "error":
    #         st.rerun()  
    
