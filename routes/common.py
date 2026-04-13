from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, select_data
from models.models import User, Student, Course, Enrollment, Homework, Lesson, Submission, Attendance
from schemas.schemas import UserCreate, UserPatch


router = APIRouter()

@router.get('/')
async def root():
    return {'message': 'You have entered the main page'}

@router.get('/users')
async def get_users(session: AsyncSession = Depends(get_session)):
    #Вызываем асинхронную функцию, чтобы посмотреть всю таблицу
    return await select_data(model=User, session=session)

@router.post('/users')
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = User(**user.model_dump())

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

@router.patch('/users/{user_id}')
async def patch_user(user: UserPatch, session: AsyncSession = Depends(get_session)):
    pass

@router.get('/courses')
async def get_courses(session: AsyncSession = Depends(get_session)):
    #Вызываем асинхронную функцию, чтобы посмотреть всю таблицу
    return await select_data(model=Course, session=session)

@router.get('/enrollments')
async def get_enrollments(session: AsyncSession = Depends(get_session)):
    return await select_data(model=Enrollment, session=session)

@router.get('/studentsss')
async def get_students(session: AsyncSession = Depends(get_session)):
    return await select_data(model=Student, session=session)

@router.get('/homeworks')
async def get_homeworks(session: AsyncSession = Depends(get_session)):
    return await select_data(model=Homework, session=session)

@router.get('/lessons')
async def get_lessons(session: AsyncSession = Depends(get_session)):
    return await select_data(model=Lesson, session=session)

@router.get('/submissions')
async def get_submissions(session: AsyncSession = Depends(get_session)):
    return await select_data(model=Submission, session=session)

@router.get('/attendance')
async def get_attendance(session: AsyncSession = Depends(get_session)):
    return await select_data(model=Attendance, session=session)