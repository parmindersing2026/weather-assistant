from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

# In memory storage
todos = []

#Request model for creating a todo
class TodoCreate(BaseModel):
    task:str

# Request model for updating a todo
class TodoUpdate(BaseModel):
    task:str
    completed:bool


#CREATE
@app.post("/todos")
def create_todo(todo: TodoCreate):
    new_todo = {
        "id": len(todos) + 1,
        "task":todo.task,
        "completed": False
    }

    todos.append(new_todo)
    return new_todo

#READ ALL
@app.get("/todos")
def get_todos():
    return todos

# Completed todos
@app.get("/todos/completed")
def get_completed_todos():
    completed_todos = []
    for todo in todos:
        if todo["completed"] == True:
            completed_todos.append(todo)
    return completed_todos

#READ ONE
@app.get("/todos/{id}")
def get_todo(id:int):
    for todo in todos:
        if todo["id"] == id:
            return todo
    return {
        "error":"Todo not found"
    }
#UPDATE
@app.put("/todos/{id}")
def update_todo(id:int, todo_update:TodoUpdate):
    for todo in todos:
        if todo['id'] == id:
            todo['task'] = todo_update.task
            todo['completed'] = todo_update.completed

            return todo
    return { "error":"Todo not found"}

#DELETE
@app.delete("/todos/{id}")
def delete_todo(id:int):
    for todo in todos:
        if todo["id"] == id:
            todos.remove(todo)
            return {"message":"Todo deleted"}
    return {
        "error":"Todo not found"
    }

# HOME PAGE
@app.get("/")
def home():
    return { "message":"Todo API is running"}

