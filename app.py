import streamlit as st
from utils.doc_parser import parse_document
from utils.summarizer import summarize_text
from utils.qa import answer_question, generate_challenge_questions, evaluate_user_answer
from utils.memory import ChatMemory
import io
import os

st.set_page_config(page_title="SmartDoc Assistant", layout="wide")

# Add custom CSS for extra polish: Google font, glassmorphism, animated buttons
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="stApp"]  {
        font-family: 'Inter', sans-serif;
    }
    body {
        background-image: url('https://images.unsplash.com/photo-1644030692053-7af7d152471a?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .stApp {
        background: rgba(20, 24, 31, 0.92);
        color: #f4f6fb;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4F8EF7 0%, #1CB5E0 100%);
        color: #fff;
        border-radius: 10px;
        padding: 0.6em 1.7em;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 8px rgba(76, 110, 245, 0.08);
        transition: background 0.2s, box-shadow 0.2s, transform 0.15s;
        font-size: 1.1em;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb 0%, #1CB5E0 100%);
        color: #fff;
        box-shadow: 0 4px 16px rgba(76, 110, 245, 0.16);
        transform: translateY(-2px) scale(1.04);
    }
    .stTextInput>div>div>input {
        background: #23293a;
        color: #f4f6fb;
        border-radius: 8px;
        border: 1.5px solid #4F8EF7;
        font-size: 1.1em;
        padding: 0.6em;
    }
    .stRadio>div>label {
        color: #f4f6fb;
        font-weight: 500;
    }
    .stMarkdown, .stInfo, .stSuccess, .stError, .stWarning {
        background: rgba(36, 44, 60, 0.85);
        border-radius: 16px;
        padding: 1.3em 1.7em;
        margin-bottom: 1.3em;
        box-shadow: 0 4px 24px 0 rgba(36, 44, 60, 0.10);
        backdrop-filter: blur(8px);
        border: 1.5px solid rgba(79, 142, 247, 0.08);
    }
    .stSubheader, .stHeader, .stTitle {
        color: #4F8EF7;
        letter-spacing: 0.5px;
        font-weight: 700;
        text-shadow: 0 2px 8px rgba(76, 110, 245, 0.08);
    }
    .stInfo {
        border-left: 4px solid #1CB5E0;
    }
    .stSuccess {
        border-left: 4px solid #4F8EF7;
    }
    .stError {
        border-left: 4px solid #e04f5f;
    }
    .stWarning {
        border-left: 4px solid #f7b731;
    }
    .stCodeBlock, .stCode {
        background: #23293a !important;
        color: #f4f6fb !important;
        border-radius: 8px !important;
        font-size: 1em !important;
        padding: 0.8em 1.1em !important;
    }
    .stFileUploader {
        background: rgba(36, 44, 60, 0.92);
        border-radius: 16px;
        padding: 1.3em 1.7em;
        margin-bottom: 1.3em;
        box-shadow: 0 4px 24px 0 rgba(36, 44, 60, 0.10);
        border: 1.5px solid rgba(79, 142, 247, 0.08);
        backdrop-filter: blur(8px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 SmartDoc Assistant")
st.write("Upload a research paper, report, or technical document (PDF/TXT) and interact with it using AI-powered reasoning.")

# Session state for memory and document
def get_memory():
    if 'memory' not in st.session_state:
        st.session_state.memory = ChatMemory()
    return st.session_state.memory

def clear_memory():
    if 'memory' in st.session_state:
        st.session_state.memory.clear()

def is_feedback_positive(feedback):
    feedback_lower = feedback.lower()
    # Only positive if contains 'correct', 'good job', or 'well done' and does NOT contain 'incorrect' or 'not correct'
    positive = any(word in feedback_lower for word in ["correct", "good job", "well done"])
    negative = any(word in feedback_lower for word in ["incorrect", "not correct"])
    return positive and not negative

def main():
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    # Reset challenge state if a new file is uploaded
    if uploaded_file is not None:
        if 'last_uploaded_filename' not in st.session_state or st.session_state['last_uploaded_filename'] != uploaded_file.name:
            st.session_state['last_uploaded_filename'] = uploaded_file.name
            if 'challenge' in st.session_state:
                del st.session_state['challenge']
    if uploaded_file:
        file_type = uploaded_file.type.split("/")[-1]
        if file_type == "plain":
            file_type = "txt"
        elif file_type == "pdf":
            file_type = "pdf"
        else:
            st.error("Unsupported file type.")
            return
        # Parse document
        file_bytes = io.BytesIO(uploaded_file.read())
        document = parse_document(file_bytes, file_type)
        st.session_state['document'] = document
        # Auto-summary
        with st.spinner("Summarizing document..."):
            summary = summarize_text(document)
        st.subheader("Auto Summary (≤150 words)")
        st.info(summary)
        mode = st.radio("Choose an interaction mode:", ["Ask Anything", "Challenge Me"])
        st.markdown("---")
        memory = get_memory()
        if mode == "Ask Anything":
            st.subheader("Ask Anything")
            if 'ask_anything_question' not in st.session_state:
                st.session_state['ask_anything_question'] = ""
            question = st.text_input("Type your question about the document:", value=st.session_state['ask_anything_question'], key="ask_anything_input")
            if st.button("Get Answer") and question:
                with st.spinner("Thinking..."):
                    answer, snippet = answer_question(document, question, memory.get())
                memory.add(question, answer)
                st.session_state['ask_anything_question'] = ""  # Clear the input box
                st.experimental_rerun()
            else:
                st.session_state['ask_anything_question'] = question
            if len(memory.get()) > 0:
                st.markdown("**Chat History:**")
                for i, (q, a) in enumerate(memory.get()):
                    st.markdown(f"**Q{i+1}:** {q}")
                    st.markdown(f"**A{i+1}:** {a}")
            if st.button("Clear Memory"):
                clear_memory()
                st.experimental_rerun()
        elif mode == "Challenge Me":
            st.subheader("Challenge Me")
            if 'challenge' not in st.session_state:
                with st.spinner("Generating questions..."):
                    questions = generate_challenge_questions(document)
                st.session_state['challenge'] = {
                    'questions': questions,
                    'user_answers': ["", "", ""],
                    'feedback': [None, None, None],
                    'correct': [None, None, None],
                    'attempts': [0, 0, 0],
                    'completed': False
                }
            challenge = st.session_state['challenge']
            total_correct = 0
            for idx, q in enumerate(challenge['questions']):
                st.markdown(f"**Q{idx+1}: {q}**")
                ans_key = f"ans_{idx}"
                user_input = st.text_input(f"Your answer to Q{idx+1}", value=challenge['user_answers'][idx], key=ans_key)
                challenge['user_answers'][idx] = user_input
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button(f"Check Q{idx+1}", key=f"eval_{idx}"):
                        if not user_input.strip():
                            st.warning("Please enter an answer before checking.")
                        else:
                            with st.spinner("Evaluating answer..."):
                                feedback, snippet = evaluate_user_answer(document, q, user_input)
                            challenge['feedback'][idx] = (feedback, snippet)
                            challenge['attempts'][idx] += 1
                            if is_feedback_positive(feedback) and user_input.strip():
                                challenge['correct'][idx] = True
                            else:
                                challenge['correct'][idx] = False
                if challenge['feedback'][idx]:
                    feedback, snippet = challenge['feedback'][idx]
                    if challenge['correct'][idx] and user_input.strip():
                        st.success(f"✅ User's answer: {user_input}\n\nEvaluation: Correct.\n\nJustification: {feedback}")
                        st.info(f"Supporting Snippet:")
                        st.code(snippet)
                    elif not user_input.strip():
                        st.warning("Please enter an answer before checking.")
                    else:
                        st.error(f"❌ User's answer: {user_input}\n\nEvaluation: Incorrect or incomplete.\n\nJustification: {feedback}")
                        st.info(f"Supporting Snippet:")
                        st.code(snippet)
                        if challenge['attempts'][idx] < 3:
                            st.info(f"You can try again! (Attempt {challenge['attempts'][idx]}/3)")
                        else:
                            st.warning("No more attempts left for this question.")
                if challenge['correct'][idx]:
                    total_correct += 1
            if all(x is not None for x in challenge['correct']):
                challenge['completed'] = True
            if challenge['completed']:
                st.markdown(f"---\n### Challenge Complete! You got **{total_correct} out of 3** correct.")
                if st.button("Try New Challenge"):
                    del st.session_state['challenge']
                    st.experimental_rerun()

if __name__ == "__main__":
    main() 