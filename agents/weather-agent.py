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

#  Structured Output Prompting:- Given Direct Instruction to the model with more than one example and structured response format.

available_tools = {
    'get_weather': get_weather
}

SYSTEM_PROMPT = """
    
    You're on AI Assistant in resolving user query using chain of thoughts. 
    You have to work on START, PLAN, ACTION, OBSERVE and OUTPUT mode.
    You need to first PLAN what need to be done. The PLAN can be multiple steps.
    
    Once you think enough then give me output.
    
    Rules:- 
    - Strictly follow the given JSON Format
    - Only run one step at a time
    - The sequence of step is START (where user gives on INPUT), PLAN (That can be multiple times.), ACTION( function calling based on the user query), OBSERVE (understand the tool result) and finally OUTPUT (which is going to display to the user.)
    - Guide the user based on the weather info that what precautions you should have to follow if any situation you are contacting the weather.
    
    
    Output JSON Format:- 
    
    {
        'step': 'START' | 'PLAN' | 'ACTION' | 'OBSERVE' | 'OUTPUT',
        'content': 'string'
    }
    
    Available Tools:
    - get_weather(city: str): Takes a city name as an input and returns the current weather for the city
    
    Example:- 
    
    Q:- How to make chai?
    Answer:- 
    START: { 'step': 'START', 'content': 'How to make chai?' }
    PLAN: { 'step': 'PLAN', 'content': 'User is asking cooking related question.' }
    PLAN: { 'step': 'PLAN', 'content': 'For making tea we have to bring water, milk, sugar and tea leaves.' }
    PLAN: { 'step': 'PLAN', 'content': 'First we need to boil water.' }
    PLAN: { 'step': 'PLAN', 'content': 'Then add tea leaves into the boiling water.' }
    PLAN: { 'step': 'PLAN', 'content': 'Now, add sugar according to the water.' }
    PLAN: { 'step': 'PLAN', 'content': 'After that, pour milk into the mixture.' }
    PLAN: { 'step': 'PLAN', 'content': 'Let it boil for 2 - 3 minutes so flavor mixes well.' }
    PLAN: { 'step': 'PLAN', 'content': 'Finally, strain the tea into a cup.' }
    PLAN: { 'step': 'PLAN', 'content': 'Tea is ready to be served hot.' }
    OUTPUT: { 'step': 'OUTPUT', 'content': 'Boil water, add tea leaves, sugar and milk boil for 2 - 3 minutes, strain and serve hot.' }
    
    Q:- What is the weather of mumbai?
    Answer:- 
    START: { 'step': 'START', 'content': 'What is the weather of mumbai?' }
    PLAN: { 'step': 'PLAN', 'content': 'Seems like user is interested in weather report.' }
    PLAN: { 'step': 'PLAN', 'content': 'First I have to see the list of available tools to check the any tool available for solving this query.' }
    PLAN: { 'step': 'PLAN', 'content': 'Yes, we have a tool of get_weather to get the weather info.' }
    PLAN: { 'step': 'PLAN', 'content': 'Now, I have to check how many parameters it should accepts.' }
    PLAN: { 'step': 'PLAN', 'content': 'Ok, the tool of get_weather accept only one parameter which is city name of find the latest weather report.' }
    ACTION: { 'step': 'ACTION', 'tool': 'get_weather', 'input': 'mumbai' }
    OBSERVE: { 'step': 'OBSERVE', 'tool': 'get_weather', 'input': 'mumbai', 'output': '30c' }
    PLAN: { 'step': 'PLAN', 'content': 'ok, The current weather of delhi is 30c.' }
    OUTPUT: { 'step': 'OUTPUT', 'content': 'Mumbai weather is 30 degree celcius. Drink Water on time and maintain hydration level.' }

"""

message_history = [
    { 'role': 'system', 'content': SYSTEM_PROMPT },
]

while True:
    user_query = input("👤: ")
    message_history.append({ 'role': 'user', 'content': user_query })

    while True:
        response = client.chat.completions.create(
            model='gemini-3.5-flash',
            messages=message_history,
            response_format={ 'type': 'json_object' }
        )

        raw_result = response.choices[0].message.content  
        message_history.append({ 'role': 'assistant', 'content': raw_result })
        parsed_result = json.loads(raw_result)
        
        if parsed_result.get('step') == 'START':
            print(f"🔥: {parsed_result.get('content')}")
            continue
        
        if parsed_result.get('step') == 'PLAN':
            print(f"🧠: {parsed_result.get('content')}")
            continue
        
        if parsed_result.get('step') == 'ACTION':
            tool_name = parsed_result.get('tool')
            tool_input = parsed_result.get('input')
            
            print(f'🔨 Tool name: {tool_name}, Input: {tool_input}')
            
            # function_name(function_input)
            if available_tools.get(tool_name, False) != False:
                tool_output = available_tools[tool_name](tool_input)
                
                print(f'🔨 Tool name: {tool_name}, Output: {tool_output}')
                
                message_history.append({ 'role': 'assistant', 'content': json.dumps({ 'step': 'OBSERVE','tool': tool_name, 'input': tool_input, 'output': tool_output }) })
                continue
        
        if parsed_result.get('step') == 'OUTPUT':
            print(f"🤖: {parsed_result.get('content')}")
            break




