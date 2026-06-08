from fastapi import FastAPI
import requests
app = FastAPI()

def get_weather(city):
    url = f'https://wttr.in/{city}?format=%C+%t'
    response = requests.get(url)
    return response.text

@app.get("/weather/{city}")
def weather(city:str):
    return{
        "City":city,
        "Weather":get_weather(city)
    }