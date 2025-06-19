import os
import groq
from dotenv import load_dotenv
import re

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# Helper: Find supporting snippet
def find_supporting_snippet(document, answer, window=50):
    # Find the answer in the document and return a snippet around it
    idx = document.lower().find(answer.lower()[:20])
    if idx == -1:
        return "[Reference not found in document]"
    start = max(0, idx - window)
    end = min(len(document), idx + window)
    return document[start:end]

# Q&A with justification
def answer_question(document, question, chat_history=None):
    context = f"Document:\n{document[:3000]}..."  # Truncate for token limit
    history = ""
    if chat_history:
        for q, a in chat_history:
            history += f"Q: {q}\nA: {a}\n"
    prompt = (
        f"You are a research assistant. Use ONLY the provided document. "
        f"Answer the question, justify with a reference (e.g., 'This is supported by paragraph 3...'), "
        f"and provide the supporting snippet.\n\n{context}\n\n{history}\nQ: {question}\nA:"
    )
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.3,
    )
    answer = response.choices[0].message.content.strip()
    # Try to extract a snippet from the document
    snippet = find_supporting_snippet(document, answer)
    return answer, snippet

# Improved Challenge question generation (stricter, no intro text)
def generate_challenge_questions(document):
    prompt = (
        "Generate exactly three clear, self-contained, logic-based or comprehension-focused questions based on the following document. "
        "Each question must be a full English sentence, at least 10 words, self-contained, and end with a question mark. Do not output phrases, incomplete sentences, or any introductory text. Output ONLY the three questions, each on a new line, numbered 1, 2, 3.\n\nDocument:\n" + document[:3000]
    )
    for _ in range(3):  # Try up to 3 times to get 3 good questions
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7,
        )
        # Extract numbered questions
        lines = response.choices[0].message.content.split('\n')
        questions = []
        for line in lines:
            line = line.strip()
            # Only keep lines that start with a number, are at least 10 words, and end with a question mark
            if re.match(r'^\d+\.', line) and len(line.split()) >= 10 and line.endswith('?'):
                # Remove the leading number and dot
                q = re.sub(r'^\d+\.\s*', '', line)
                questions.append(q)
        if len(questions) >= 3:
            return questions[:3]
    # Fallback: show message if not enough valid questions
    return ["[Could not generate a valid question for this document. Please try another document or re-upload.]"] * 3

# Evaluate user answer
def evaluate_user_answer(document, question, user_answer):
    prompt = (
        f"Document:\n{document[:3000]}...\n\n"
        f"Question: {question}\nUser's Answer: {user_answer}\n"
        f"Evaluate the user's answer. Is it correct? Justify your evaluation with a reference to the document and provide the supporting snippet."
    )
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3,
    )
    feedback = response.choices[0].message.content.strip()
    snippet = find_supporting_snippet(document, feedback)
    return feedback, snippet 