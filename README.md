# SmartDoc Assistant

An AI-powered assistant for research summarization and document reasoning. Upload a PDF or TXT, get a concise summary, ask questions, or challenge yourself with logic-based questions—all with document-grounded answers and justifications.

## Features
- **Document Upload:** PDF/TXT support
- **Auto Summary:** ≤150 words
- **Ask Anything:** Contextual Q&A with references
- **Challenge Me:** Logic-based questions, answer evaluation, and feedback
- **Memory:** Follow-up questions with context
- **Answer Highlighting:** Shows supporting document snippets
- **Modern UI:** Beautiful background, custom colors, and improved UX

## Setup Instructions
1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd SmartDoc Assistant
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Groq API key in a `.env` file:
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   ```
   - Get your key from [Groq Console](https://console.groq.com/)
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Architecture / Reasoning Flow
- **Frontend:** Streamlit for UI, file upload, and interaction modes
- **Backend/Core Logic:** Python modules for parsing, summarization, Q&A, challenge, memory, and highlighting
- **LLM:** Groq API (Llama 3) for summarization, Q&A, and logic question generation
- **Memory:** In-memory chat history for contextual follow-ups
- **Highlighting:** Snippet extraction and display for answer justification
- **Modern UI:** Custom CSS for background and color scheme

## Usage
1. Upload a PDF or TXT document.
2. View the auto-generated summary.
3. Choose "Ask Anything" to ask questions, or "Challenge Me" for logic-based questions.
4. Get answers with references and highlighted supporting text.
5. Follow up with more questions—context is preserved!

---

**Demo:** https://youtu.be/ZX482LUv2CQ

---

## License
MIT 