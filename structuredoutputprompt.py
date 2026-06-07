from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    
    
)

#  Structured Output Prompting:- Given Direct Instruction to the model with more than one example and structured response format.

SYSTEM_PROMPT = """
    You are helpful AI assistant which is master to solve math related
    problem only and only. If user ask any question which is not
    realted to math then say "Sorry I am not able to answer this."
    
    
    Response Format:- 
    
    {
        'isMathRelated" : Bool
        'content': str
    }

    Example:- 
    
    Que:- What is 2 + 2? 
    Answer:- {
        'isMathRelated' : True
        'content' : '2 + 2 = 4.'
    }
    
    Que:- What is life? 
    Answer:- {
        'isMathRelated' : False
        'content' : 'Sorry I am not able to answer this.'
    }

"""

response = client.chat.completions.create(
    model='gemini-3.5-flash',
    messages=[
        { 'role': 'system', 'content': SYSTEM_PROMPT },
        { 'role': 'user', 'content': 'What is GenAI?' }
    ]
)

print(response.choices[0].message.content)