from sqlalchemy.orm import DeclarativeBase  # базовый класс декларативной ORM в SQLAlchemy 2.0+


# Создаём базовый класс, от которого будут наследоваться все ORM-модели
class Base(DeclarativeBase):
    pass