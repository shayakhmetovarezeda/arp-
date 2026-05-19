from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Schedule Service")
schedule_db = []

class TimeSlot(BaseModel):
    course_id: int
    day: str
    time_start: str
    time_end: str

@app.post("/schedule")
def add_slot(slot: TimeSlot):
    schedule_db.append(slot)
    return {"status": "ok"}

@app.post("/check-conflict")
def check_conflict(new_slots: List[TimeSlot]):
    # Простая проверка: ищем пересечения по дню и времени
    for new in new_slots:
        for old in schedule_db:
            if old.day == new.day:
                if not (new.time_end <= old.time_start or new.time_start >= old.time_end):
                    return {"conflict": True, "conflict_with": old.course_id}
    return {"conflict": False}