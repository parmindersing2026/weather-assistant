from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_APIKEY")
)
MODEL = 'gpt-4o'
SYSTEM_PROMPT = """
You are a weather assistant.
Only answer weather-related questions.
Only answer questions about one city at a time.
If Multiple cities are requested, ask the user to provide one city.
If the question is not about weather,
politely say 'I can help with weather questions.'
"""

def get_weather(city):
    
    try:
        url=f'https://wttr.in/{city}?format=%C+%t'
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "Unable to retrieve weather information."
        return response.text
    except Exception:
         return "Weather service is unavailable."


tools = [
    {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description":"Get current weather for a city",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"City name"
                    }
                },
                "required":["city"]
            }
        }
    }
]

def ask_weather_assistant(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                'role':'system',
                "content":SYSTEM_PROMPT
            },
            {
            'role':'user',
            'content':question
        }],
        tools=tools
    )

    message = (response.choices[0].message)
    if not message.tool_calls:
        return message.content
    tool_call = message.tool_calls[0]

    # print(tool_call)
    try:
         arguments = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
         return "Sorry, I couldn't process the weather request."
    # print(arguments)
    weather = get_weather(arguments["city"])
    # print(weather)

    messages = [
        {
            'role':'system',
            'content': SYSTEM_PROMPT
        },
        {
            'role':'user','content':question
        },
        response.choices[0].message,
        {
            'role':'tool',
            'tool_call_id':tool_call.id,
            'content':weather
        }
    ]

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return final_response.choices[0].message.content

def main():
    while True:
        question = input("You: Ask me About Weather: ")

        if question.strip().lower() == "exit":
                break
        answer = ask_weather_assistant(question)
        print("Assistant: ",answer)


if __name__ == "__main__":
     main()