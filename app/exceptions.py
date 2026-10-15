from fastapi import HTTPException, status


USER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователь не найден",
)

INCORRECT_DATA_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Неверный email или пароль",
)

USER_UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь не авторизован",
)

USER_ALREADY_CREATED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь уже существует"
)

INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Невалидный токен",
)

INTERNAL_SERVER_ERROR_EXCEPTION = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка сервера",
)

PERMISSION_DENIED_TO_DELETE_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Удалить аккаунт может только админ",
)

PERMISSION_DENIED_TO_CHANGE_DATA_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Вы не можете изменять чужой аккаунт",
)

PERMISSION_DENIED_TO_CREATE_ADMIN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Недостаточно прав на создание админа",
)

PERMISSION_DENIED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Недостаточно прав доступа",
)

INVALID_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={"code": "UNAUTHORIZED", "message": "Invalid token"},
)

INCORRECT_DATA = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"code": "NOT_FOUND", "message": "Incorrect email or password"},
)