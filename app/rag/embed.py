import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def get_embedding(text: str):
    resp = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    return resp.data[0].embedding