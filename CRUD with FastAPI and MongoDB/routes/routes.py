from typing import List
from dotenv import dotenv_values
from fastapi import APIRouter, status, Request, Body
from fastapi.encoders import jsonable_encoder

from models.student import (
    StudentSchema,
    UpdateStudentModel,
    ResponseModel,
    ErrorResponseModel,
)

config = dotenv_values(".env")
collection = config["COLLECTION_NAME"]


""" Database CRUD Operations. """

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "CRUD Operations using FastAPI and MongoDB."}


# Retrieve all students present in the database.
@router.get(
    "/student",
    response_description="Retrieve All Students",
    response_model=List[StudentSchema],
)
async def get_all_students(request: Request):
    return list(request.app.database[collection].find(limit=100))


# Retrieve a student with a matching ID.
@router.get("/student/{id}", response_description="Retrieve Student ID")
async def get_student_data(id: str, request: Request):
    if (student := request.app.database[collection].find_one({"_id": id})) is not None:
        return ResponseModel([student], f"Student ID: {id} Retrieved Successfully.")

    return ErrorResponseModel(
        "An error occurred", 404, "Student ID {0} doesn't exist.".format(id)
    )


# Add a new student to the database.
@router.post(
    "/student/add",
    response_description="Add Student Data",
    status_code=status.HTTP_201_CREATED,
)
async def add_student_data(request: Request, student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = request.app.database[collection].insert_one(student)
    return ResponseModel(
        [request.app.database[collection].find_one({"_id": new_student.inserted_id})],
        "Student Added Successfully.",
    )


# Update a student with a matching ID.
@router.put("/student/{id}", response_description="Update Student Data")
async def update_student_data(
    id: str, request: Request, student: UpdateStudentModel = Body(...)
):
    if updated_student := {k: v for k, v in student.dict().items() if v is not None}:
        update_result = request.app.database[collection].update_one(
            {"_id": id}, {"$set": updated_student}
        )

        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred", 404, "Student ID {0} doesn't exist.".format(id)
            )

    if (
        exist_user := request.app.database[collection].find_one({"_id": id})
    ) is not None:
        return ResponseModel([exist_user], f"Student ID: {id} Updated Successfully.")

    return ErrorResponseModel(
        "An error occurred", 404, "Student ID {0} doesn't exist.".format(id)
    )


# Delete a student from the database with a matching ID.
@router.delete("/student/{id}", response_description="Delete Student Data")
async def delete_student_data(id: str, request: Request):
    deleted_student = request.app.database[collection].delete_one({"_id": id})

    if deleted_student.deleted_count == 1:
        return ResponseModel(
            f"Student ID: {id} removed.", "Student Deleted Successfully."
        )

    return ErrorResponseModel(
        "An error occurred", 404, "Student ID {0} doesn't exist.".format(id)
    )
