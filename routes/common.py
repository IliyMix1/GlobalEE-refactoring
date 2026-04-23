from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, select_all_records, select_record, select_record_by_email, create_record, patch_record
from models.models import User, Student, Course, Enrollment, Homework, Lesson, Submission, Attendance
from schemas.schemas import UserCreate, UserPatch, CourseCreate, CoursePatch, Auth, AuthUserCreate, AuthStudentCreate
from auth import verify_password, hash_password


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

@router.post('/reg')
async def registration(schema: Auth, session: AsyncSession = Depends(get_session)):
    #Ищем запись по введённой почте
    same_student = await select_record_by_email(email=schema.email, model=Student, session=session)

    #Проверяем, есть ли уже аккаунт с такой почтой
    if same_student is not None:
        raise HTTPException(status_code=409, detail='Email already taken')
    
    #Хэшируем пароль
    password = hash_password(schema.password)

    #Собираем данные, которые, будем отправлять в БД
    user_data = AuthUserCreate(
        hashed_password=password,
        role='student'
    )
    #Отправляем данные и сразу же получаем объект(чтобы использовать его id)
    user = await create_record(model=User, schema=user_data, session=session)

    #Собираем данные, которые, будем отправлять в БД
    student_data = AuthStudentCreate(
        user_id=user.user_id,
        email=schema.email,
        first_name='Jane',
        last_name='Doe'
    )
    #Отправляем данные
    await create_record(model=Student, schema=student_data, session=session)

    return {'message': 'New account successfully created'}

@router.post('/login')
async def login(schema: Auth, session: AsyncSession = Depends(get_session)):
    #Ищем запись по введённой почте
    same_student = await select_record_by_email(email=schema.email, model=Student, session=session)

    #Проверяем, есть ли уже аккаунт с такой почтой
    if same_student is None:
        raise HTTPException(status_code=401, detail='Account with this email does not exists')
    
    user = await select_record(id=same_student.user_id, model=User, session=session)

    is_verified = verify_password(password_plain=schema.password, password_hashed=user.hashed_password)
    if is_verified:
        return {'message': "You've entered successfully"}
    else:
        raise HTTPException(status_code=401, detail='Password is wrong')

    