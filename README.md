# 📌 TalentScout - AI-Powered Screening Chatbot  

![TalentScout Banner](https://github.com/Durai-Bharath/TalentScout/raw/main/Banner/banner.png)

🚀 **TalentScout** is an AI-powered **screening chatbot** designed to streamline the **technical hiring process**. It dynamically generates **skill-based interview questions**, evaluates candidate responses using **vector similarity**, and provides an **automated assessment score**.  

---

## 🛠 Features  

### 🔹 Job Openings & Application Management  
- Displays available job roles dynamically.  
- Allows candidates to **apply for a job** through a structured form.  

### 🤖 AI-Powered Screening Chatbot  
- Generates **customized interview questions** for multiple skills per job.  
- Adapts question difficulty based on the candidate's responses.  
- Prevents **question repetition** to maintain interview integrity.  

### 🎯 Intelligent Answer Evaluation  
- Utilizes **vector similarity-based evaluation** to compare candidate responses.  
- Dynamically updates scores based on accuracy.  
- Tracks **wrong attempts** and adjusts difficulty accordingly.  

### 📊 Performance Assessment & Leaderboard  
- Displays **final assessment scores** after the interview.  
- Maintains a **leaderboard** of candidates who scored above `0`, ranked in descending order.  
- Provides recruiters with a **shortlist of top candidates**.  

---

## 🏗 Tech Stack  

| Category        | Technologies Used |
|----------------|------------------|
| Frontend       | **Streamlit** |
| Backend        | **Python, SQLite** |
| AI/ML         | **LLM (Openrouter API), Vector Similarity** |
| Database       | **SQLite3** |
| Deployment     | **Streamlit Cloud / Other Hosting Services** |

---

## 🚀 Installation & Setup  

### 🔧 Prerequisites  
Ensure you have the following installed:  
- **Python 3.8+**  
- **pip** (Python package manager)  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/Durai-Bharath/TalentScout.git
cd TalentScout
```

### 2️⃣ Create a Virtual Environment  
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate    # Windows
```


### 3️⃣ Install Dependencies  
```sh
pip install -r requirements.txt
```

### 4️⃣ Initialize the Database
```sh
python init_db.py
```
### 5️⃣ Run the Application
```sh
streamlit run app.py
```

## 🚀 Future Enhancements  

✅ **Support for multiple LLM models** (including self-hosted models)  
✅ **Integration with ATS (Applicant Tracking System)**  
✅ **Improved NLP-based answer evaluation**  
✅ **Adaptive difficulty & question weighting system**  

