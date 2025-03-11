import uvicorn
import streamlit as st
import json
from pathlib import Path
import random

# Define questions
QUESTIONS_FILE = "questions.json"
def load_questions():
    if Path(QUESTIONS_FILE).exists():
        with open(QUESTIONS_FILE, "r") as f:
            return json.load(f)
    return []

# Save default questions if not exist
def save_default_questions():
    default_questions = [
        {"question": "What is the capital of France?", "options": ["Paris", "Berlin", "Rome", "Madrid"], "answer": "Paris", "difficulty": "Easy"},
        {"question": "Which programming language is known for AI development?", "options": ["Python", "Java", "C++", "Ruby"], "answer": "Python", "difficulty": "Easy"},
        {"question": "What is the output of 2 ** 3 in Python?", "options": ["5", "6", "8", "9"], "answer": "8", "difficulty": "Medium"},
        {"question": "Which data structure uses LIFO principle?", "options": ["Queue", "Stack", "Linked List", "Heap"], "answer": "Stack", "difficulty": "Medium"},
        {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(n^2)", "O(log n)", "O(1)"], "answer": "O(log n)", "difficulty": "Hard"}
    ]
    if not Path(QUESTIONS_FILE).exists():
        with open(QUESTIONS_FILE, "w") as f:
            json.dump(default_questions, f)

# Quiz App class
class QuizApp:
    def __init__(self):
        self.questions = load_questions()
        self.score = 0
        self.current_question = 0
        self.question_order = random.sample(range(len(self.questions)), len(self.questions))  # Random order

    def run(self):
        st.title("📝 Advanced Quiz App")
        
        if "score" not in st.session_state:
            st.session_state.score = 0
        if "current_question" not in st.session_state:
            st.session_state.current_question = 0
        if "question_order" not in st.session_state:
            st.session_state.question_order = self.question_order
        
        if st.session_state.current_question < len(self.questions):
            q_index = st.session_state.question_order[st.session_state.current_question]
            q = self.questions[q_index]
            st.subheader(f"{q['difficulty']} - {q['question']}")
            choice = st.radio("Select an answer:", q["options"], key=f"q{st.session_state.current_question}")
            
            if st.button("Submit Answer"):
                if choice == q["answer"]:
                    st.session_state.score += 3 if q['difficulty'] == "Hard" else (2 if q['difficulty'] == "Medium" else 1)
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong! The correct answer is {q['answer']}")
                
                st.session_state.current_question += 1
                st.rerun()
        else:
            st.write(f"**Quiz completed! Your final score: {st.session_state.score}/{sum(3 if q['difficulty']=='Hard' else (2 if q['difficulty']=='Medium' else 1) for q in self.questions)}**")
            if st.button("Restart Quiz"):
                st.session_state.score = 0
                st.session_state.current_question = 0
                st.session_state.question_order = random.sample(range(len(self.questions)), len(self.questions))
                st.rerun()

if __name__ == "__main__":
    save_default_questions()
    app = QuizApp()
    app.run()
