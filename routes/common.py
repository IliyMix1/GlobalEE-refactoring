from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, select_all_records, select_record, select_record_by_email, create_record, patch_record
from models.models import User, Student, Course, Enrollment, Homework, Lesson, Submission, Attendance
from schemas.schemas import UserCreate, UserPatch, CourseCreate, CoursePatch, UserAuth
from auth import verify_password


router = APIRouter()

@router.get('/')
async def root():
    return {'message': 'You have entered the main page'}

@router.get('/studentsss')
async def get_students(session: AsyncSession = Depends(get_session)):
    return await select_all_records(model=Student, session=session)

@router.get('/homeworks')
async def get_homeworks(session: AsyncSession = Depends(get_session)):
    return await select_all_records(model=Homework, session=session)

@router.get('/lessons')
async def get_lessons(session: AsyncSession = Depends(get_session)):
    return await select_all_records(model=Lesson, session=session)

@router.get('/submissions')
async def get_submissions(session: AsyncSession = Depends(get_session)):
    return await select_all_records(model=Submission, session=session)

@router.get('/attendance')
async def get_attendance(session: AsyncSession = Depends(get_session)):
    return await select_all_records(model=Attendance, session=session)

@router.post('/auth')
async def login(schema: UserAuth, session: AsyncSession = Depends(get_session)):
    #Берём запись из students и достаём id по email
    student = await select_record_by_email(email=schema.email, model=Student, session=session)

    if student is None:
        raise HTTPException(status_code=409, detail='Email does not exists')

    #Берём запись из users и достаёт хэш пароля по id
    user = await select_record(id=student.user_id, model=User, session=session)
    return verify_password(password_plain=schema.password, password_hashed=user.hashed_password)

    