import streamlit as st
from Openrouter.learning_req import get_learning_req

# Initialize session state
if "user_question" not in st.session_state:
    st.session_state.user_question = ""  # Store user input persistently

if "loading" not in st.session_state:
    st.session_state.loading = False  # Track loading state

if "response" not in st.session_state:
    st.session_state.response = None  # Store bot response persistently

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Store chat history persistently

def goBack():
    st.session_state.chat_history.clear()
    st.session_state.user_question = ""
    st.session_state.response = None
    st.session_state.loading = False
    st.session_state.learning_chat = False
    st.session_state.chat_started = False

def clearInput():
    if st.session_state.user_question != "":
        st.session_state.loading = True
        st.session_state.chat_history.clear()
        st.session_state.chat_history.append((st.session_state.user_question, st.session_state.response))
        st.session_state.user_question = ""

# Chatbot UI
def learningChat():
    st.markdown("""
        <style>
            .bot-msg {background-color: #f0f2f6; padding: 10px; border-radius: 10px;margin-bottom: 10px;}
            .user-msg {background-color: #e1f5fe; padding: 10px; border-radius: 10px;margin-bottom: 10px;}
            .msg-container {margin-bottom: 10px;}
            .stTextInput>div>div>input {
                height: 40px !important;  /* Adjust input height */
            }
            .stButton>button {
                height: 40px !important;  /* Match button height */
                margin-top: 26px !important; /* Align with input */
                background-color:#ff8c00 !important; /* Blue background */
                color: white !important; /* White text */
                border-radius: 5px !important; /* Rounded corners */
            }
        </style>
    """, unsafe_allow_html=True)

    st.button("Back", key="back_button", on_click=goBack)
    
    st.title("💡 AI Learning Chatbot")
    st.markdown("""
        Welcome to the **Learning Chatbot**! 🤖  
        🚀 *Ask me any tech-related question, and I'll help you learn!*  
        ⚠️ *Non-tech questions will not be answered.*  
    """)

    # Layout with two columns
    col1, col2 = st.columns([4, 1])

    # User Input Field (Inside col1)
    with col1:
        user_input = st.text_input(
            "Ask a tech-related question...",
            key="user_question",
            placeholder="Type your question here...",
            on_change=clearInput
        )
        
        if st.session_state.chat_history == []:
            st.warning("⚠️ Please enter a question to continue.")
       
    
    # Ask Button (Inside col2)
    with col2:
        st.button(
            "Ask 🚀",
            key="ask_button",
            on_click= clearInput
        )  
            
        
    # Display loading indicator
    if st.session_state.loading:
        
        with st.spinner("🤖 Thinking..."):
            askQuestion()
            st.session_state.loading = False  # Reset loading state after response

    # Display response if available
    for user_input, response in st.session_state.chat_history:
        st.markdown(f'<div class="user-msg"><b>You:</b> {user_input}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-msg"><b>🤖:</b> {response}</div>', unsafe_allow_html=True)
        st.session_state.clear_input = True
        
        
def askQuestion():
    user_input = st.session_state.chat_history[-1][0]
    if user_input:
        try:
            response = get_learning_req(user_input)
            # Filter out non-tech responses
            if "non-tech" in response.lower() or "not relevant" in response.lower():
                response = "⚠️ This is not related to technology. Please ask tech-related questions!"
        except Exception as e:
            response = "❌ Oops! Something went wrong. Please try again."

        st.session_state.response = response
        st.session_state.chat_history.clear()
        st.session_state.chat_history.append((user_input,response))    
    else:
        st.warning("⚠️ Please enter a question to continue.")
    
