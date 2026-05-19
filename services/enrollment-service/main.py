from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Enrollment Service")
enrollments_db = []


class EnrollmentRequest(BaseModel):
    student_id: int
    course_id: int


# В Docker сервисы общаются по именам контейнеров на порту 8000
COURSE_URL = "http://course-service:8000"
SCHEDULE_URL = "http://schedule-service:8000"


@app.post("/enroll")
async def enroll(req: EnrollmentRequest):
    async with httpx.AsyncClient() as client:
        # 1. Проверяем, существует ли курс
        resp = await client.get(f"{COURSE_URL}/courses/{req.course_id}")
        if resp.status_code == 404:
            raise HTTPException(400, "Курс не найден")

        # 2. Проверяем расписание (в демо считаем, что конфликтов нет)
        resp_schedule = await client.post(f"{SCHEDULE_URL}/check-conflict", json=[])
        if resp_schedule.json().get("conflict"):
            raise HTTPException(409, "Конфликт расписания!")

    # 3. Сохраняем запись
    record = {"student_id": req.student_id, "course_id": req.course_id, "status": "enrolled"}
    enrollments_db.append(record)
    return {"message": "Успешно записан!", "data": record