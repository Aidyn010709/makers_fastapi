from pydantic import BaseModel


class CourseConst(BaseModel):
    
    # Course
    COURSE_NOT_FOUND: str = "Курс не найден"
    COURSE_TITLE: str = "Название курса"
    SHORT_DESCRIPTION: str = "Описание"
    START_COURSE: str = "Начало курса"
    FINISH_COURSE: str = "Конец курса"
    DURATION: str = "Длительность курса"
    IS_ACTIVE: str = 'Активный курс'
    IS_DEACTIVATE: str = 'Неактивированные курсы'
    PRICE: str = 'Цена курса'

CONSTANTS = CourseConst()