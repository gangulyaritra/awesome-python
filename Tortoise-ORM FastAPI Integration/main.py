from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import Student_Pydantic, StudentIn_Pydantic, Student


app = FastAPI(title="Tortoise-ORM FastAPI Integration")


class Status(BaseModel):
    message: str


@app.get("/student/all", response_model=List[Student_Pydantic])
async def get_students():
    return await Student_Pydantic.from_queryset(Student.all())


@app.get(
    "/student/get/{student_id}",
    response_model=Student_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_student(student_id: int):
    return await Student_Pydantic.from_queryset_single(Student.get(id=student_id))


@app.post("/student/add", response_model=Student_Pydantic)
async def create_student(student: StudentIn_Pydantic):
    student_obj = await Student.create(**student.dict(exclude_unset=True))
    return await Student_Pydantic.from_tortoise_orm(student_obj)


@app.put(
    "/student/update/{student_id}",
    response_model=Student_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_student(student_id: int, student: StudentIn_Pydantic):
    await Student.filter(id=student_id).update(**student.dict(exclude_unset=True))
    return await Student_Pydantic.from_queryset_single(Student.get(id=student_id))


@app.delete(
    "/student/delete/{student_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
)
async def delete_student(student_id: int):
    deleted_count = await Student.filter(id=student_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"Student {student_id} doesn't exist"
        )
    return Status(message=f"Student {student_id} Deleted Successfully.")


register_tortoise(
    app,
    db_url="sqlite://studentdb.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
