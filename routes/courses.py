from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, select_all_records, select_record, create_record, patch_record
from models.models import User, Student, Course, Enrollment, Homework, Lesson, Submission, Attendance
from schemas.schemas import UserCreate, UserPatch, CourseCreate, CoursePatch, CourseOut


courses_router = APIRouter(prefix='/courses', tags=['Courses'])


@courses_router.get('/', response_model=list[CourseOut])
async def get_courses(session: AsyncSession = Depends(get_session)):
    #Вызываем асинхронную функцию, чтобы посмотреть всю таблицу
    return await select_all_records(model=Course, session=session)


@courses_router.get('/{course_id}', response_model=CourseOut)
async def get_course(course_id: int, session: AsyncSession = Depends(get_session)):
    record = await select_record(id=course_id, model=Course, session=session)

    if record is None:
        raise HTTPException(status_code=404, detail='Record not found')

    return record

@courses_router.post('/', response_model=CourseOut)
async def create_course(course: CourseCreate, session: AsyncSession = Depends(get_session)):
    return await create_record(schema=course, model=Course, session=session)


@courses_router.patch('/{course_id}', response_model=CourseOut)
async def patch_course(course_id: int, course: CoursePatch, session: AsyncSession = Depends(get_session)):
    record = await patch_record(id=course_id, schema=course, model=Course, session=session)

    if record is None:
        raise HTTPException(status_code=404, detail='Record not found')
    
    return record