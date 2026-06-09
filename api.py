from fastapi import FastAPI
from pydantic import BaseModel
from assistant import ask_weather_assistant

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(request:QuestionRequest): 
    # Here request is a variable and it has any name like data, user_input. Same we need to use in ask_weather_assistant function assigned to variable answer
    answer = ask_weather_assistant(
        request.question
    )

    return {
        "answer":answer
    }

@app.get("/")
def home():
    return {
        "message":"Weather Assistant API is Running...."
    }