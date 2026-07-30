from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Your in-memory "database"
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

# Endpoint to get ALL tasks
@app.get("/tasks")
def get_all_tasks():
    return tasks

# Endpoint to get a SINGLE task
@app.get("/tasks/{id}")
def get_task(id: int):
    # Search for the task by id
    for task in tasks:
        if task["id"] == id:
            return task
    
    # If the loop finishes and no task is found, return the 404 error
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})