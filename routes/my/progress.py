#Для эндпоинтов
from fastapi                import APIRouter, Depends, HTTPException
from schemas.schemas        import StudentOut, StudentPatch
#Для интеграции с PostgreSQL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy             import select
from database               import get_session, patch_record
from models.models          import Student, Enrollment, Submission, Attendance
#Зависимости
from dependencies           import get_current_user

my_router = APIRouter(prefix='/my', tags=['Progress'])

@my_router.get('/profile', response_model=StudentOut)
async def get_profile(user = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    '''Даём пользователю взглянуть на его контакнтные данные'''
    result = await session.execute(
        select(Student).where(Student.user_id == user.user_id)
    )
    student = result.scalar_one_or_none()

    return student

@my_router.patch('/profile', response_model=StudentOut)
async def patch_profile(data: StudentPatch, user = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    '''Позволяем пользователю изменить свои контактные данные'''
    record = await patch_record(id=user.user_id, model=Student, schema=data, session=session)

    if record is None:
        raise HTTPException(status_code=404, detail='Record not found')
    
    return record

@my_router.get('/{enrollment_id}/submissions')
async def get_submissions_by_enrollment(enrollment_id: int, user = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    #Проверяем есть ли такой id в БД
    result = await session.execute(
        select(Enrollment).where(Enrollment.enrollment_id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    
    if enrollment is None:
        raise HTTPException(status_code=404, detail='Enrollment not found')

    if enrollment.user_id != user.user_id:
        raise HTTPException(status_code=403, detail='Course is not owned')

    #Достаём из БД все сданные работы по id
    result = await session.execute(
        select(Submission).where(Submission.enrollment_id == enrollment_id)
    )
    submissions = result.scalars().all()
    return submissions

@my_router.get('/{enrollment_id}/attendance')
async def get_attendance_by_enrollment(enrollment_id: int, user = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    #Проверяем есть ли такой id в БД
    result = await session.execute(
        select(Enrollment).where(Enrollment.enrollment_id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(status_code=404, detail='Enrollment not found')

    if enrollment.user_id != user.user_id:
        raise HTTPException(status_code=403, detail='Course is not owned')

    result = await session.execute(
        select(Attendance).where(Attendance.enrollment_id == enrollment_id)
    )
    attendance = result.scalars().all()
    return attendance

