#Импортируем библиотеки
from pydantic import BaseModel, field_validator, Field
from fastapi  import FastAPI, HTTPException, Query
from typing   import Literal, Annotated
import logging
import uvicorn
import json

#Настраиваем логирование
logging.basicConfig(level=logging.INFO, 
                    filename="py_log.log", 
                    filemode="a", 
                    format="%(asctime)s %(levelname)s %(message)s", 
                    encoding='utf-8')
logger = logging.getLogger(__name__)

#Создаём объект класса FastAPI
app = FastAPI()

#Создаём шаблон класс, для удобства работы со студентом
class StudentBase(BaseModel):
    name:   str
    grade:  Literal[9, 10, 11]
    tariff: Literal['mini', 'standard', 'pro']

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

class StudentFilters(BaseModel):
    #Настраиваем значение фильтра через Field: задаём дефолтное значение и интервал
    grade: int | None = Field(default=None, ge=9, le=11)
    #Говорим, что фильтр может быть либо одним из 3 конкретных значений, либо никаким
    tariff: Literal['mini', 'standard', 'pro'] | None = None


def load_students() -> dict:
    '''Читаем файл и возвращаем словарь словарей'''
    #Пробуем прочитать файл
    try:
        with open('students.json', 'r') as f:
            students = json.load(f)
            return students
        
    #Если файла не существует - создаём его
    except FileNotFoundError:
        #Создаём шаблон
        template = {'1': {
            'id': 1,
            'name': 'Jon Snow',
            'grade': 11,
            'tariff': 'mini',
        }}

        with open('students.json', 'w') as f:
            json.dump(template, f, indent=4)
        
        return template

def save_changes(students: dict) -> None:
    '''Сохраняем изменения в файл'''
    with open('students.json', 'w') as f:
        json.dump(students, f, indent=4)
    logger.info('Changes saved')

def check_for_duplicates(student: dict) -> bool:
    '''Проверяем на дубликаты'''
    students = load_students()

    any_duplicates = False
    #Проходимя по каждому ученику в БД и сверяем их данные с данными нового ученика
    for dicts in students.values():
        if dicts['name'] == student['name'] and dicts['grade'] == student['grade'] and dicts['tariff'] == student['tariff']:
            
            logger.warning(f'Duplicate-student creation rejected: id={dicts["id"]}')
            any_duplicates = True
            
    return any_duplicates

@app.get('/')
def root() -> str:
    return "You've entered the main page"

@app.get('/students')
def get_all_students(filters: Annotated[StudentFilters, Query()]) -> list:    #Annotated говорит, что вкачестве аргумента используем объект и считаем его query param
    '''Отображаем всю базу данных'''
    #Загружаем всех учеников из файла в словарь вида (id: {info})
    students = load_students()
    #Собираем список с информацией о всех студентах
    students_list = list(students.values())

    #Выкидываем из списка учеников с несовпадающим классом
    if filters.grade is not None:
        students_list = [student for student in students_list if student['grade'] == filters.grade]
    #Выкидываем из списка учеников с несовпадающим тарифом
    if filters.tariff is not None:
        students_list = [student for student in students_list if student['tariff'] == filters.tariff]

    if not students_list:
        raise HTTPException(status_code=404, detail='No students were found')

    return students_list

@app.get('/students/{id}')
def get_student(id: int) -> dict:
    '''Отображаем конкретного ученика по id'''
    students = load_students()
    #Если в словаре есть студент с таким id - возвращаем его
    if students.get(str(id)):
        return students[str(id)]
    else:
        logger.warning(f'Student not found: id={id}')
        raise HTTPException(status_code=404, detail='Student not found')

@app.post('/students/', status_code=201)
def create_student(student: StudentCreate) -> dict:
    '''Добавляем ученика'''
    students = load_students()

    #Проверяем на дублирование
    new_student = student.model_dump()  #Заносим данные из модели в словрь
    if check_for_duplicates(student=new_student):
        raise HTTPException(status_code=409, detail='Duplicate-student creation rejected')

    #Составляем список всех id, находим максимальный и увеличиваем его на 1
    ids = [int(i) for i in students.keys()]
    new_id = max(ids) + 1 
    #Добавляем нового ученика в словарь
    students[str(new_id)] = {
        'id': new_id,
        'name': student.name,
        'grade': student.grade,
        'tariff': student.tariff,
    }
    save_changes(students=students)

    logger.info(f'Student was added: id={new_id}')
    return students[str(new_id)]

@app.delete('/students/{id}')
def delete_student(id: int) -> dict:
    students = load_students()

    #Если не найден ученик с таким id - возвращаем ошибку
    if students.get(str(id)) is None:
        logger.warning(f'Student not found')
        raise HTTPException(status_code=404, detail='Student not found')
    
    #Удаляем студента
    del students[str(id)]
    
    logger.info(f'Student was deleted: id={id}')
    save_changes(students)
    return {'message': 'Student was deleted'}

@app.put('/students/{id}')
def put_student_data(id: int, student: StudentPut) -> dict:
    '''Обновляем всю информацию об ученике'''
    students = load_students()

    new_student = students.get(str(id))
    if new_student is None:
        logger.warning('Student not found')
        raise HTTPException(status_code=404, detail='Student not found')
    
    #Обновляем всю информацию
    students[str(id)] = {
        'id': id,
        'name': student.name,
        'grade': student.grade,
       'tariff': student.tariff,
    }
    #Проверяем на дублирование
    if check_for_duplicates(student=students[str(id)]):
        raise HTTPException(status_code=409, detail='Duplicate-student creation rejected')
    
    #Сохраняем изменения, если всё хорошо
    save_changes(students=students)
    logger.info(f'Student data was changed entirely: id={id}')
    return students[str(id)]

@app.patch('/students/{id}')
def patch_student_data(id: int, student: StudentPatch):
    '''Обновляем часть информации об ученике'''
    students = load_students()
    
    current_student = students.get(str(id))
    if current_student is None:
        logger.warning('Student not found')
        raise HTTPException(status_code=404, detail='Student not found')
    
    updated_student = current_student.copy()
    #Сохраняем словарь с изменениями в новую переменную(аргумент функции выкидывает значения по умолчанию, оставляя только изменённое)
    update_data = student.model_dump(exclude_unset=True)
    updated_student.update(update_data)
    
    #Проверяем на дублирование
    if check_for_duplicates(student=updated_student):
        raise HTTPException(status_code=409, detail='Duplicate-student creation rejected')
    
    students[str(id)] = updated_student
    #Сохраняем изменения, если всё хорошо
    save_changes(students=students)
    logger.info(f'Student data was changed partly: id={id}')
    return students[str(id)]

#Поднимаем сервер
if __name__ == '__main__':
    uvicorn.run('server:app', reload=True)
