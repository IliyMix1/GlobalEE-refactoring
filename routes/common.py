from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, select_all_records, create_record, patch_record
from models.models import User, Student, Course, Enrollment, Homework, Lesson, Submission, Attendance
from schemas.schemas import UserCreate, UserPatch, CourseCreate, CoursePatch


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