from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    """
    Базовий клас для всіх моделей SQLAlchemy.
    Містить метадані для створення таблиць.
    """
    pass
