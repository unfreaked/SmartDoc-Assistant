import os
import groq
from dotenv import load_dotenv

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text(text):
    # Truncate text to reduce processing time
    max_chars = 6000  # Reduce context size for faster processing
    truncated_text = text[:max_chars] + ("..." if len(text) > max_chars else "")
    
    prompt = "Summarize the following document in 130 to 150 words. Be concise, focus on key points, and do not exceed 150 words.\n\n" + truncated_text
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Updated model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=350,  # Allow for a longer summary
        temperature=0.3,
    )
    return response.choices[0].message.content.strip() 