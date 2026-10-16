from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Conf(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

class AppConfig(Conf):
    IS_PROD: bool = False
    FRONTEND_URL: str = "http://localhost:3000"


class CORSConfig(Conf):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]


class IntegrationConfig(Conf):
    API_KEY_POD: str = ""
    POD_URL: str = "https://opendata.mkrf.ru/v2"


class PostgresConfig(Conf):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "db"
    POSTGRES_USER: str = "delfin"
    POSTGRES_PASSWORD: str = "1234"
    ECHO: bool = False

    @computed_field
    @property
    def POSTGRES_URL_ASYNC(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
        )


class JwtConfig(Conf):
    JWT_SECRET_KEY: str = "changeme"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    app: AppConfig = AppConfig()
    cors: CORSConfig = CORSConfig()
    pg_database: PostgresConfig = PostgresConfig()
    jwt: JwtConfig = JwtConfig()


settings = Settings()
