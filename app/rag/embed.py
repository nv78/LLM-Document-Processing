import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def get_embedding(text: str):
    # new for openai>=1.0.0
    resp = openai.embeddings.create(
        model=settings.EMBED_MODEL,      # e.g. "text-embedding-3-small"
        input=text
    )
    # the response shape is a dict, not an object
    return resp.data[0].embedding
