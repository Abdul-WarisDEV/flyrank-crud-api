from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# 1. Define the expected shape of the incoming data
class TaskCreate(BaseModel):
    title: str | None = None  # Default to None so we can manually catch empty submissions

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": False},
    {"id": 3, "title": "Complete Stage 2", "done": True}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_all_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

# --- NEW STAGE 3 CODE BELOW ---

@app.post("/tasks")
def create_task(task_in: TaskCreate):
    # Validation: If title is missing or empty, return 400 Bad Request
    if not task_in.title or not task_in.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is missing or empty"})
    
    # Calculate the next free ID
    if len(tasks) > 0:
        next_id = max(task["id"] for task in tasks) + 1
    else:
        next_id = 1
        
    # Construct the new task dictionary
    new_task = {
        "id": next_id,
        "title": task_in.title.strip(),
        "done": False
    }
    
    # Add it to the list
    tasks.append(new_task)
    
    # Return 201 Created with the new task data
    return JSONResponse(status_code=201, content=new_task)