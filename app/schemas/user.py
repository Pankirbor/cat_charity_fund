from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Класс схемы для представления объекта пользователя."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Класс схемы для создания объекта пользователя."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Класс схемы для обновления данных объекта пользователя."""

    pass
