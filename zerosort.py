from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model='gemini-3.5-flash',
    messages=[
        { 'role': 'system', 'content': 'You are helpful AI assistant which is master to solve math related problem only and only. If user ask any question which is not realted to math then say "Sorry I am not able to answer this."' },
        { 'role': 'user', 'content': 'What is 2 + 2?' }
    ]
)

print(response.choices[0].message.content)