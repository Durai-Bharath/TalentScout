import streamlit as st
import pandas as pd
from DB_Services.read import getAllUsers,getJobById  # Function to fetch candidates

def leaderboard():
    st.title("🏆 Leaderboard - Top Performers")
    
    # Fetch candidates who attended the interview
    candidates = getAllUsers()  # Fetch data from DB or file
    if not candidates or len(candidates) == 0:
        st.warning("No candidates have taken the interview yet!")
        return
    
    job = getJobById(candidates[0][6])
   
    # Convert to DataFrame
    columns = ["Name", "Email","Phone","Year of Exp","Location","Role","Score"] 
    df = pd.DataFrame(candidates,columns=columns)
    
  
    # df.columns = ["User ID", "Name", "Email","Phone","Year of Exp","Location","Role","Score"]
    # Reset index for better display
    df.reset_index(drop=True, inplace=True)

    # Display the leaderboard
    st.dataframe(df, use_container_width=True)


