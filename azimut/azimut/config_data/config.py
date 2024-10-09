from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    engine: str
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class Config:
    db: DatabaseConfig


def load_config(path) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        db=DatabaseConfig(
            engine=env('ENGINE'),
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD'),
        )
    )


def get_env_secret_key(path) -> str:
    env: Env = Env()
    env.read_env(path)
    return env('SECRET_KEY')
