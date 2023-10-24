class InvalidNameException(Exception):
    """Исключение при создании некорректном заполнении поля name."""

    pass


class DuplicateNameException(Exception):
    """Исключение при попытке создать объект с неуникальным значением поля name."""

    pass


class InvalidDataFieldException(Exception):
    """Исключение при использовании некорректных данных."""

    pass


class InvalidPatchException(Exception):
    """Исключение при попытке редактировании объекта."""

    pass


class InvalidDeleteException(Exception):
    """Исключение при попытке удаления объекта."""

    pass
