import re
from tortoise import fields, models
from tortoise.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from tortoise.contrib.pydantic import pydantic_model_creator


class Student(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, null=False)
    surname = fields.CharField(max_length=20, null=False)
    email = fields.CharField(
        max_length=30,
        validators=[RegexValidator("^[a-zA-Z0-9]+@essex.ac.uk$", re.I)],
        unique=True,
    )
    mobile = fields.CharField(
        max_length=10, validators=[MinLengthValidator(10)], unique=True
    )
    degree = fields.CharField(max_length=10, default="Bachelor")
    course = fields.CharField(max_length=50)
    semester = fields.IntField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    gpa = fields.DecimalField(
        max_digits=1,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
    )
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    def username(self) -> str:
        return f"{self.name.lower()}.{self.surname.lower()}.{self.id}"

    class PydanticMeta:
        computed = ["username"]


Student_Pydantic = pydantic_model_creator(Student, name="Student")
StudentIn_Pydantic = pydantic_model_creator(
    Student, name="StudentIn", exclude_readonly=True
)
