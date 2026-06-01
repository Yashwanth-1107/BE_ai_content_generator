from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

class ContentRequest(BaseModel):
    topic: str
    technology: str
    content_type: str
    tone: str

@app.get("/")
def home():
    return {"msg": "you are Home"}

@app.post("/generate")
def generate_content(data: ContentRequest):

    prompt = f"""
    Generate a {data.content_type}

    Topic: {data.topic}
    Technology: {data.technology}
    Tone: {data.tone}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "content": response.choices[0].message.content
    }