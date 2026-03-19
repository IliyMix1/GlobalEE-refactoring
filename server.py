#Импортируем библиотеки
from fastapi  import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
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
    grade:  int
    tariff: str

    #Проводим валидацию класса ученика
    @field_validator('grade')
    @classmethod
    def validate_grade(cls, value: int) -> int:
        if value not in (9, 10, 11):
            raise ValueError('Grade must be 9, 10 or 11')
        else:
            return value
    
    #Проводим валидацию тарифа ученика
    @field_validator('tariff')
    @classmethod
    def validate_tariff(cls, value: str) -> str:
        value = value.lower() 
        if value != 'mini' and value != 'standard' and value != 'pro':
            raise ValueError('There is no such tariff. Pick "mini" or "standard" or "pro"')
        else:
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
    grade:  int | None = None
    tariff: str | None = None

    #Проводим валидацию класса ученика
    @field_validator('grade')
    @classmethod
    def validate_grade(cls, value: int | None) -> int | None:
        if value not in (9, 10, 11):
            raise ValueError('Grade must be 9, 10 or 11')
        else:
            return value
    
    #Проводим валидацию тарифа ученика
    @field_validator('tariff')
    @classmethod
    def validate_tariff(cls, value: str | None) -> str | None:
        value = value.lower() 
        if value != 'mini' and value != 'standard' and value != 'pro':
            raise ValueError('There is no such tariff. Pick "mini" or "standard" or "pro"')
        else:
            return value


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
        template = {1: {
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

def check_for_duplicates(student: StudentOut) -> bool:
    '''Проверяем на дубликаты'''
    students = load_students()

    any_duplicates = False
    #Проходимя по каждому ученику в БД и сверяем их данные с данными нового ученика
    for dicts in students.values():
        if dicts['name'] == student.name and dicts['grade'] == student.grade and dicts['tariff'] == student.tariff:
            
            logger.warning(f'Duplicate-student creation rejected: id={dicts['id']}')
            any_duplicates = True
            
    return any_duplicates

@app.get('/')
def root() -> str:
    return "You've entered the main page"

@app.get('/students')
def get_all_students() -> list:        #Возвращаем список словарей
    '''Отображаем всю базу данных'''
    students = load_students()
    students_list = []
    for student in students.values():
        students_list.append(student)

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
    if check_for_duplicates(student=student):
        raise HTTPException(status_code=409, detail='Duplicate-student creation rejected')

    #Составляем список всех id, находим максимальный и увеличиваем его на 1
    ids = [int(i) for i in students.keys()]
    new_id = max(ids) + 1 
    #Добавляем нового ученика в словарь
    students[new_id] = {
        'id': new_id,
        'name': student.name,
        'grade': student.grade,
        'tariff': student.tariff,
    }
    save_changes(students=students)

    logger.info(f'Student was added: id={new_id}')
    return students[new_id]

@app.delete('/students/{id}')
def delete_student(id: int) -> dict:
    students = load_students()

    for ids in students.keys():
        if id == int(ids):
            del students[ids]

            logger.info(f'Student was deleted: id={ids}')
            save_changes(students)
            return {'message': 'Student was deleted'}

    else:
        logger.warning(f'Student not found')
        raise HTTPException(status_code=404, detail='Student not found')

@app.put('/students/{id}')
def put_student_data(id: int, student: StudentPut) -> dict:
    '''Обновляем всю информацию об ученике'''
    students = load_students()
    #Проверяем на дублирование
    if check_for_duplicates(student=student):
        raise HTTPException(status_code=409, detail='Duplicate-student creation rejected')

    for ids in students.keys():
        if id == int(ids):
            
            #Обновляем всю информацию
            students[ids] = {
                'id': id,
                'name': student.name,
                'grade': student.grade,
                'tariff': student.tariff,
            }
            
            #Сохраняем изменения, если всё хорошо
            save_changes(students=students)
            logger.info(f'Student data was changed entirely: id={id}')
            return students[ids]
    else:
        logger.warning('Student not found')
        raise HTTPException(status_code=404, detail='Student not found')

@app.patch('/students/{id}')
def patch_student_data(id: int, student: StudentPatch):
    '''Обновляем часть информации об ученике'''
    students = load_students()
    #Проверяем на дублирование
    if check_for_duplicates(student=student):
        raise HTTPException(status_code=409, detail='Duplicate-student creation rejected')
    
    for ids in students.keys():
        if id == int(ids):
            #Обновляем всю информацию
            if student.name:
                students[ids]['name'] = student.name
            if student.grade:
                students[ids]['grade'] = student.grade
            if student.tariff:
                students[ids]['tariff'] = student.tariff
            
            #Сохраняем изменения, если всё хорошо
            save_changes(students=students)
            logger.info(f'Student data was changed partly: id={id}')
            return students[ids]
    else:
        logger.warning('Student not found')
        raise HTTPException(status_code=404, detail='Student not found')

#Поднимаем сервер
if __name__ == '__main__':
    uvicorn.run('server:app', reload=True)
