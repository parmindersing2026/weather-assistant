from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_APIKEY")
)

def get_weather(city):
    url=f'https://wttr.in/{city}?format=%C+%t'
    response = requests.get(url)
    return response.text

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

question = "What's the weather in Mohali?"

response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role':'user','content':question}],
    tools=tools
)
message = response.choices[0].message
tool_call = message.tool_calls[0]

arguments = json.loads(tool_call.function.arguments)
weather = get_weather(arguments['city'])
print(weather)

messages = [
    {'role':'user','content':question},
    response.choices[0].message,
    {'role':'tool',
     'tool_call_id':tool_call.id,
     "content":weather
     }
]

final_response = client.chat.completions.create(
    model='gpt-4o',
    messages=messages
)

print(final_response.choices[0].message.content)