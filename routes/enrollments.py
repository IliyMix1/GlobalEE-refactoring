# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from database import get_session, select_all_records, select_record, create_record, patch_record
# from models.models import User, Student, Course, Enrollment, Homework, Lesson, Submission, Attendance
# from schemas.schemas import EnrollmentCreate, EnrollmentPatch, EnrollmentOut

# enrollments_router = APIRouter(prefix='/enrollments', tags=['Enrollments'])


# @enrollments_router.get('/', response_model=list[EnrollmentOut])
# async def get_all_enrollments(session: AsyncSession = Depends(get_session)):
#     return await select_all_records(model=Enrollment, session=session)


# @enrollments_router.get('/{enrollment_id}', response_model=EnrollmentOut)
# async def get_enrollment(enrollment_id: int, session: AsyncSession = Depends(get_session)):
#     record = await select_record(id=enrollment_id, model=Enrollment, session=session)

#     if record is None:
#         raise HTTPException(status_code=404, detail='Record not found')
    
#     return record


# #НАДО ССЫЛАТЬСЯ НА STUDENTS, А НЕ USERS
# @enrollments_router.post('/', response_model=EnrollmentOut)
# async def create_enrollment(schema: EnrollmentCreate, session: AsyncSession = Depends(get_session)):
#     #Валидируем id юзера
#     user = await session.get(User, schema.user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail='User not found')
    
#     #Валидируем id курса
#     course = await session.get(User, schema.course_id)
#     if course is None:
#         raise HTTPException(status_code=404, detail='Course not found')

#     return await create_record(model=Enrollment, schema=schema, session=session)


# #НАДО ССЫЛАТЬСЯ НА STUDENTS, А НЕ USERS
# @enrollments_router.patch('/{enrollment_id}', response_model=EnrollmentOut)
# async def patch_enrollment(enrollment_id: int, schema: EnrollmentPatch, session: AsyncSession = Depends(get_session)):
#     #Валидируем id юзера
#     user = await session.get(User, schema.user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail='User not found')
    
#     #Валидируем id курса
#     course = await session.get(User, schema.course_id)
#     if course is None:
#         raise HTTPException(status_code=404, detail='Course not found')
    
#     return await patch_record(id=enrollment_id, model=Enrollment, schema=schema, session=session)