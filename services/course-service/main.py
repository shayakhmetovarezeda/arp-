from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Course Service")
courses_db = []

class Course(BaseModel):
    id: int
    title: str
    teacher: str
    prerequisites: List[str] = []

@app.get("/courses", response_model=List[Course])
def get_courses():
    return courses_db

@app.post("/courses")
def create_course(course: Course):
    courses_db.append(course)
    return {"status": "ok", "course": course}

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for c in courses_db:
        if c.id == course_id:
            return c
    raise HTTPException(status_code=404, detail="Курс не найден")