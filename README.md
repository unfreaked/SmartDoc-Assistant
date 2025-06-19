# SmartDoc Assistant

## Project Overview
SmartDoc Assistant is an AI-powered web application designed to help users quickly understand and reason through large documents such as research papers, legal files, or technical manuals. By leveraging advanced language models, it enables users to upload PDF or TXT files, receive concise summaries, ask free-form questions, and challenge themselves with logic-based questions—all with document-grounded answers and justifications. The app features a modern, professional UI for a seamless and engaging user experience.

## Features
- **Document Upload:** PDF/TXT support
- **Auto Summary:** 130–150 word summary
- **Ask Anything:** Contextual Q&A with references
- **Challenge Me:** Logic-based questions, answer evaluation, and feedback
- **Memory:** Follow-up questions with context
- **Answer Highlighting:** Shows supporting document snippets
- **Modern UI:** Beautiful background, custom colors, and improved UX


**[Watch the demo video](https://youtu.be/ZX482LUv2CQ)**

## Setup Instructions
**Requirements:**
- Python 3.9+
- [Groq API key](https://console.groq.com/)

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Set your Groq API key in a `.env` file:**
```env
GROQ_API_KEY=your-groq-api-key-here
```

**Run the app:**
```bash
streamlit run app.py
```

## Usage Examples
**Upload a document:**
- Use the web UI to drag and drop a PDF or TXT file.

**Ask Anything:**
- Type a question in the "Ask Anything" box and get a contextual answer with a supporting snippet.

**Challenge Me:**
- Switch to "Challenge Me" mode to answer logic-based questions generated from your document. Get instant feedback and justifications.

**(Optional) API Example:**
If you want to call the backend logic from Python:
```python
from utils.summarizer import summarize_text
summary = summarize_text(open('yourfile.txt').read())
print(summary)
```

## Architecture Diagram
```
+-------------------+      +-------------------+      +-------------------+
|   Streamlit UI    | <--> |   Python Backend  | <--> |   Groq LLM API    |
| (Frontend + UX)   |      | (Parsing, Logic)  |      | (Llama 3 Model)   |
+-------------------+      +-------------------+      +-------------------+
        |                        |                        |
        |----> File Upload ----->|                        |
        |<--- Summary/Q&A/------>|                        |
        |     Challenge          |                        |
```

## License
MIT 
