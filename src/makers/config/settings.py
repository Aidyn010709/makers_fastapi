from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable, Type, Tuple

from pydantic import BaseSettings, validator, PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = list(PostgresDsn.allowed_schemes) + ["postgresql+asyncpg"]


class Settings(BaseSettings):
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
    APP_DIR = BASE_DIR / "makers"

    CURRENT_API_VERSION = "/v1"
    API_ROUTE_STR: str = "/api"

    SERVER_NAME: str = "MAKERS_BACKEND"
    SECRET_KEY: str = "MIIFRjCCBC6gAwIBAgIQCIdSGhpikQCjOIY154XoqzANBgkqhkiG9w0BAQsFADBN"

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # JWT
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 3
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # SMTP
    MJ_APIKEY_PUBLIC: str = ""
    MJ_APIKEY_PRIVATE: str = ""

    URL_FRONTEND_ACTIVATION_CODE: str = ""
    URL_FRONTEND_RESET_PASSWORD: str = ""
    URL_FRONTEND_ACTIVATE_COMPANY: str = ""

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "makers"

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1"
    POSTGRES_DB: str = "makers"
    POSTGRES_PORT: str = "5432"

    # Paybox configurations
    VITE_FP_MERCHANT_PAYMENT_KEY: str = ""
    VITE_FP_MERCHANT_ID: int = 0
    PAYBOX_INIT_URL: str = ""
    PG_INTERNSHIP_RESULT_URL: str = ""
    PG_SUBSCRIPTION_RESULT_URL: str = ""
    PG_INTERVIEW_RESULT_URL: str = ""
    PG_INTERVIEW_REQUEST_AMOUNT: int = 0

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 15
    SQLALCHEMY_DATABASE_URI: Optional[AsyncPostgresDsn] = None
    PUBLISHER_URL: str = ""

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=values.get("POSTGRES_PORT"),
        )

    USE_TZ: bool = True
    TZ = "Asia/Bishkek"

    MEDIA_ROOT: str = str(APP_DIR / "media")

    EXCEPTIONS_TO_HANDLE: List[Tuple[Type[Exception], Callable]] = []

    # gmail config
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.mail.ru"

    class Config:
        env_file = "./.env"


settings = Settings()
