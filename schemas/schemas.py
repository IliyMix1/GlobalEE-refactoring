from typing import Literal
from pydantic import BaseModel, field_validator, Field
from datetime import date

#Создаём шаблон класс, для удобства работы со студентом
class StudentBase(BaseModel):
    name:   str = Field(min_length=2, max_length=50)
    grade:  Literal[9, 10, 11]
    tariff: Literal['mini', 'standard', 'pro']

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        #Проверяем, не стала ли строка пустой после удаления лишних пробелов
        if len(value) < 2:
            raise ValueError('First name should not be empty')
        
        #Проверяем, есть ли в имени цифры
        for symbol in value:
            if symbol.isdigit():
                raise ValueError('First name should not contain digits')
        return value
    
#Вариация класса для работы с выводом
class StudentOut(StudentBase):
    id: int

#Вариация класса для создания студента
class StudentCreate(StudentBase):
    pass

#Вариация класса для ПОЛНОГО изменения информации о студенте
class StudentPut(StudentBase):
    pass

#Вариация класса для ЧАСТИЧНОГО изменения информации о студенте
class StudentPatch(BaseModel):
    #Наши переменные имеют либо INT/STR тип, либо None, а по умолчанию все они равны None
    name:   str | None = None
    grade:  Literal[9, 10, 11] | None = None
    tariff: Literal['mini', 'standard', 'pro'] | None = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if value is None:
            return value
        
        value = value.strip()
        #Проверяем, не стала ли строка пустой после удаления лишних пробелов
        if len(value) < 2:
            raise ValueError('Name should not be empty')

        #Проверяем, есть ли в имени цифры
        for symbol in value:
            if symbol.isdigit():
                raise ValueError('Name should not contain digits')
        return value
    

class UserCreate(BaseModel):
    hashed_password: str = Field(min_length=2)
    role: Literal['student', 'admin']

class UserPatch(BaseModel):
    hashed_password: str | None = None
    role: Literal['student', 'admin'] | None = None

class CourseCreate(BaseModel):
    name: str = Field(min_length=2)

class CoursePatch(BaseModel):
    name: str | None = None

class CourseOut(CourseCreate):
    course_id: int
    created_at: date