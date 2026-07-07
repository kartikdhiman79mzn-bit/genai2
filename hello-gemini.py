from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model='gemini-3.5-flash',
    messages=[
        { 'role': 'system', 'content': 'You are helpful AI Assistant.' },
        { 'role': 'user', 'content': 'Hello How are you?' }
    ]
)

print(response.choices[0].message.content)