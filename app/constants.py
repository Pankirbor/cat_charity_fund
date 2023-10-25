# models and schemas:
GREATER_THAN = 0
MAX_LENGTH = 100
MIN_LENGTH = 1
DEFAULT_AMOUNT = 0

# endpoints:
TAGS_METADATA = [
    {
        "name": "Charity Projects",
        "description": "Операции над благотворительными фондами.",
    },
    {
        "name": "Donations",
        "description": "Операции по взносу и просмотру своих пожертвований.",
    },
    {
        "name": "Auth",
        "description": "Регистрация пользователей. Операции входа и выхода.",
    },
    {
        "name": "Users",
        "description": "Операции с пользователями.",
    },
]

# error message:
NAME_DUPLICATE = "Проект с таким именем уже существует!"
NOT_FOUND_PROJECT = "Проект не найден!"
CLOSE_PROJECT = "Закрытый проект нельзя редактировать!"
INVALID_FULL_AMOUNT = (
    "Невозможно устанавить новую требуемую сумму, так как она меньше уже собранной."
)
INVALID_NAME = "Имя или описание не может быть пустой строкой."
MIN_FULL_AMOUNT_EXCEPTION = "Требуемая сумма не может быть меньше или равняться нулю."
INVALID_DELETE = "В проект были внесены средства, не подлежит удалению!"
NOT_USER_DELETE = "Удаление пользователей запрещено!"
