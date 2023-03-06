import uuid
import datetime
from typing import Dict
from pydantic import BaseModel, Field, constr, confloat

"""
We define two Pydantic Schemas, i.e., `StudentSchema` and `UpdateStudentModel` to represent how the student data will get stored in the MongoDB Database.

Pydantic Schema validates data along with serializing (JSON -> Python) and de-serializing (Python -> JSON).
"""


class StudentSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    fullname: str = Field(...)
    email: constr(max_length=30, regex="^[a-zA-Z0-9]+@essex.ac.uk$") = Field(...)
    mobile: constr(regex="^[0-9]{10}$") = Field(...)
    enrollment_date: datetime.date = Field(...)
    degree: str = Field(...)
    course: str = Field(...)
    semester: int = Field(..., gt=0, lt=9)
    gpa: Dict[constr(max_length=1, regex="[1-8]"), confloat(ge=0.0, le=4.0)] = Field(
        ...
    )

    class Config:
        schema_extra = {
            "example": {
                "_id": "",
                "fullname": "",
                "email": "email@essex.ac.uk",
                "mobile": "",
                "enrollment_date": "YYYY-MM-DD",
                "degree": "Bachelor/Master/PhD",
                "course": "",
                "semester": 1,
                "gpa": {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.0},
            }
        }


class UpdateStudentModel(BaseModel):
    fullname: str = Field(...)
    email: constr(max_length=30, regex="^[a-zA-Z0-9]+@essex.ac.uk$") = Field(...)
    mobile: constr(regex="^[0-9]{10}$") = Field(...)
    degree: str = Field(...)
    course: str = Field(...)
    semester: int = Field(..., gt=0, lt=9)
    gpa: Dict[constr(max_length=1, regex="[1-8]"), confloat(ge=0.0, le=4.0)] = Field(
        ...
    )

    class Config:
        schema_extra = {
            "example": {
                "fullname": "",
                "email": "email@essex.ac.uk",
                "mobile": "",
                "degree": "Bachelor/Master/PhD",
                "course": "",
                "semester": 1,
                "gpa": {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.0},
            }
        }


def ResponseModel(data, message):
    return {"data": data, "status": "Ok", "code": 200, "message": message}


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
