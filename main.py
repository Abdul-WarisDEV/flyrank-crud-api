from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")

class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": False},
    {"id": 3, "title": "Complete Stage 2", "done": True}
]

@app.get("/", summary="API Root")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="List all tasks")
def get_all_tasks():
    return tasks

@app.get("/tasks/{id}", summary="Get task by ID")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.post("/tasks", summary="Create a new task")
def create_task(task_in: TaskCreate):
    if not task_in.title or not task_in.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is missing or empty"})
    
    next_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {
        "id": next_id,
        "title": task_in.title.strip(),
        "done": False
    }
    tasks.append(new_task)
    return JSONResponse(status_code=201, content=new_task)

@app.put("/tasks/{id}", summary="Update a task")
def update_task(id: int, task_in: TaskUpdate):
    task = next((t for t in tasks if t["id"] == id), None)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
    
    if task_in.title is None and task_in.done is None:
        return JSONResponse(status_code=400, content={"error": "At least one field (title or done) must be provided"})
    
    if task_in.title is not None:
        if not task_in.title.strip():
            return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
        task["title"] = task_in.title.strip()
        
    if task_in.done is not None:
        task["done"] = task_in.done

    return task

@app.delete("/tasks/{id}", summary="Delete a task")
def delete_task(id: int):
    global tasks
    task = next((t for t in tasks if t["id"] == id), None)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
    
    tasks = [t for t in tasks if t["id"] != id]
    return JSONResponse(status_code=204, content=None)