from pydantic import AnyHttpUrl, BaseSettings, Field


class PostgresSettings(BaseSettings):
    """Postgres Settings"""

    user: str = "postgres"
    db: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    password: str = "postgres"

    class Config:
        env_prefix = "postgres_"
        allow_population_by_field_name = True

    @property
    def uri(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class <CLASSIFIED_REPO_NAME>Settings(BaseSettings):
    """<CLASSIFIED_REPO_NAME> Third Party Settings"""

    class Config:
        env_prefix = "<REPO_NAME>_"


class Settings(BaseSettings):
    """<REPO_NAME> Settings"""

    database: PostgresSettings = PostgresSettings()
    secret_key: str
    <PYTHONED_REPO_NAME>: <CLASSIFIED_REPO_NAME>Settings = <CLASSIFIED_REPO_NAME>Settings()
    release_version: str = "0.0.0"


settings = Settings()
