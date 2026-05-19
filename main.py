from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import time

app = FastAPI(
    title="Co-op Library Classroom Test API",
    description="Live target API for Module 1: Consuming APIs",
    version="1.2.0"
)

# --- Configuration ---
AUTH_ENABLED = True
VALID_TOKEN = "coop-learner-2026"
RATE_LIMIT_WINDOW = 10
MAX_REQUESTS = 5

# --- Persistence ---
templates = Jinja2Templates(directory="templates")
tasks_db = [
    {"id": 1, "title": "Learn REST Basics", "description": "Understand GET vs POST", "completed": True},
    {"id": 2, "title": "Test the API", "description": "Send a request via Tailscale", "completed": False},
]
traffic_logs = []
request_tracker = {}


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False


# --- Internal Logic ---

def log_activity(request: Request, action: str, status: int, details: str):
    client_ip = request.client.host if request.client else "Unknown"
    log_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "ip": client_ip,
        "action": action,
        "status": status,
        "details": details
    }
    traffic_logs.insert(0, log_entry)
    if len(traffic_logs) > 30: traffic_logs.pop()


def check_security_and_rate(request: Request):
    client_ip = request.client.host if request.client else "Unknown"
    now = time.time()

    # 1. Rate Limiting
    if client_ip not in request_tracker: request_tracker[client_ip] = []
    request_tracker[client_ip] = [t for t in request_tracker[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(request_tracker[client_ip]) >= MAX_REQUESTS:
        log_activity(request, f"{request.method} {request.url.path}", 429, "Rate limit exceeded")
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Slow down!")
    request_tracker[client_ip].append(now)

    # 2. Authentication Toggle
    if AUTH_ENABLED:
        auth_header = request.headers.get("Authorization")
        if not auth_header or auth_header != f"Bearer {VALID_TOKEN}":
            log_activity(request, f"{request.method} {request.url.path}", 401, "Auth Failed")
            raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid token.")


# --- UI & Dashboard ---

@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
async def dashboard_root(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/v1/internal/state", tags=["Dashboard"])
async def get_internal_state():
    return {
        "db": tasks_db,
        "logs": traffic_logs,
        "auth_status": AUTH_ENABLED
    }


# --- Student Endpoints ---

@app.get("/v1/books", tags=["Student Endpoints"])
async def get_books(request: Request, page: int = 1, limit: int = 10):
    check_security_and_rate(request)
    log_activity(request, "GET /v1/books", 200, f"Page {page}, Limit {limit}")
    return tasks_db


@app.post("/v1/books", status_code=201, tags=["Student Endpoints"])
async def create_book(task: Task, request: Request):
    check_security_and_rate(request)
    if any(t["id"] == task.id for t in tasks_db):
        log_activity(request, "POST /v1/books", 400, f"Duplicate ID: {task.id}")
        raise HTTPException(status_code=400, detail="ID already exists.")

    new_item = task.model_dump()
    tasks_db.append(new_item)
    log_activity(request, "POST /v1/books", 201, f"Created: {task.title}")
    return new_item


@app.put("/v1/books/{book_id}", tags=["Student Endpoints"])
async def update_book(book_id: int, task: Task, request: Request):
    check_security_and_rate(request)
    for idx, item in enumerate(tasks_db):
        if item["id"] == book_id:
            tasks_db[idx] = task.model_dump()
            log_activity(request, f"PUT /v1/books/{book_id}", 200, "Updated item")
            return tasks_db[idx]
    raise HTTPException(status_code=404, detail="Book not found.")


@app.delete("/v1/books/{book_id}", tags=["Student Endpoints"])
async def delete_book(book_id: int, request: Request):
    check_security_and_rate(request)
    for idx, item in enumerate(tasks_db):
        if item["id"] == book_id:
            removed = tasks_db.pop(idx)
            log_activity(request, f"DELETE /v1/books/{book_id}", 200, f"Deleted: {removed['title']}")
            return {"detail": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found.")


# --- Admin Controls ---

@app.post("/admin/toggle-auth", tags=["Admin"])
async def toggle_auth(request: Request):
    global AUTH_ENABLED
    AUTH_ENABLED = not AUTH_ENABLED
    log_activity(request, "ADMIN", 200, f"Auth toggled to {AUTH_ENABLED}")
    return {"auth_enabled": AUTH_ENABLED}