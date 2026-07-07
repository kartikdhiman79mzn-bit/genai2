from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def get_weather(city: str) -> str:
    url = f'https://wttr.in/{city}?format=%C+%t'
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The current weather of {city} is {response.text}"
    
    return "Something is wrong"


available_tools = {
    'get_weather': get_weather
}

SYSTEM_PROMPT = """
You're an AI Assistant in resolving user query using chain of thoughts. 
You have to work on START, PLAN, ACTION, OBSERVE and OUTPUT mode.
You need to first PLAN what need to be done. The PLAN can be multiple steps.

Once you think enough then give me output.

Rules:- 
- Strictly follow the given JSON Format
- Only run one step at a time
- The sequence of step is START (where user gives an INPUT), PLAN (That can be multiple times.), ACTION( function calling based on the user query), OBSERVE (understand the tool result) and finally OUTPUT (which is going to display to the user.)
- Guide the user based on the weather info that what precautions you should have to follow if any situation you are contacting the weather.

Output JSON Format:- 

{
    'step': 'START' | 'PLAN' | 'ACTION' | 'OBSERVE' | 'OUTPUT',
    'content': 'string'
}

Available Tools:
- get_weather(city: str): Takes a city name as an input and returns the current weather for the city
"""

def process_query(user_query: str):
    """Process user query and return the agent's response"""
    
    message_history = [
        { 'role': 'system', 'content': SYSTEM_PROMPT },
    ]
    
    message_history.append({ 'role': 'user', 'content': user_query })
    
    response_steps = []
    
    while True:
        response = client.chat.completions.create(
            model='gemini-3.5-flash',
            messages=message_history,
            response_format={ 'type': 'json_object' }
        )
        
        assistant_response = response.choices[0].message.content
        message_history.append({ 'role': 'assistant', 'content': assistant_response })
        
        response_json = json.loads(assistant_response)
        response_steps.append(response_json)
        
        if response_json['step'] == 'ACTION':
            tool_name = response_json['tool']
            tool_input = response_json['input']
            
            if tool_name in available_tools:
                tool_output = available_tools[tool_name](tool_input)
                observe_response = {
                    'step': 'OBSERVE',
                    'tool': tool_name,
                    'input': tool_input,
                    'output': tool_output
                }
                message_history.append({ 'role': 'user', 'content': json.dumps(observe_response) })
        
        elif response_json['step'] == 'OUTPUT':
            break
    
    return response_steps
