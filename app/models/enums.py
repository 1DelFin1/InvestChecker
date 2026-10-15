from enum import Enum


class UserRoleTypes(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"