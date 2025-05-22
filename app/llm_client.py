import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def summarize_text(text: str) -> str:
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":f"Summarize this medical note:\n{text}"}]
    )
    return resp.choices[0].message.content.strip()

def generate_answer(question: str, context: str) -> str:
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message.content.strip()