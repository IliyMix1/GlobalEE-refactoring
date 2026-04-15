from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, select_all_records, create_record, patch_record
from models.models import User, Student, Course, Enrollment, Homework, Lesson, Submission, Attendance
from schemas.schemas import UserCreate, UserPatch, CourseCreate, CoursePatch


router = APIRouter()

@router.get('/')
async def root():
    return {'message': 'You have entered the main page'}


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